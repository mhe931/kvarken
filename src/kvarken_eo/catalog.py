"""Persistent, dependency-free spatial and metadata catalog."""

import json
import sqlite3
import threading
from collections.abc import Sequence
from datetime import datetime
from pathlib import Path

from .models import EOScene
from .spatial import scene_intersects_roi, validate_bbox


class SpatialCatalog:
    """SQLite-backed scene catalog with indexed metadata and bbox pre-filtering."""

    def __init__(self, path: Path | str) -> None:
        self._connection = sqlite3.connect(path, check_same_thread=False)
        self._connection.row_factory = sqlite3.Row
        self._lock = threading.RLock()
        self._connection.execute("PRAGMA journal_mode=WAL")
        self._connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS scenes (
                scene_id TEXT PRIMARY KEY,
                platform TEXT NOT NULL,
                acquired_at TEXT NOT NULL,
                cloud_cover REAL NOT NULL,
                min_x REAL NOT NULL,
                min_y REAL NOT NULL,
                max_x REAL NOT NULL,
                max_y REAL NOT NULL,
                epsg INTEGER NOT NULL,
                footprint_json TEXT NOT NULL,
                assets_json TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_scenes_platform_time
                ON scenes(platform, acquired_at);
            CREATE INDEX IF NOT EXISTS idx_scenes_bbox
                ON scenes(min_x, max_x, min_y, max_y);
            """
        )
        self._connection.commit()

    def close(self) -> None:
        with self._lock:
            self._connection.close()

    def __enter__(self) -> "SpatialCatalog":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def index_scene(self, scene: EOScene) -> None:
        if scene.bbox is None:
            bbox = (
                min(point[0] for point in scene.footprint),
                min(point[1] for point in scene.footprint),
                max(point[0] for point in scene.footprint),
                max(point[1] for point in scene.footprint),
            )
        else:
            bbox = validate_bbox(scene.bbox)
        with self._lock:
            self._connection.execute(
                """
                INSERT INTO scenes (
                    scene_id, platform, acquired_at, cloud_cover, min_x, min_y, max_x, max_y,
                    epsg, footprint_json, assets_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(scene_id) DO UPDATE SET
                    platform=excluded.platform,
                    acquired_at=excluded.acquired_at,
                    cloud_cover=excluded.cloud_cover,
                    min_x=excluded.min_x,
                    min_y=excluded.min_y,
                    max_x=excluded.max_x,
                    max_y=excluded.max_y,
                    epsg=excluded.epsg,
                    footprint_json=excluded.footprint_json,
                    assets_json=excluded.assets_json
                """,
                (
                    scene.scene_id,
                    scene.platform,
                    scene.acquired_at.isoformat(),
                    scene.cloud_cover,
                    *bbox,
                    scene.epsg,
                    json.dumps(scene.footprint),
                    json.dumps(dict(scene.assets), sort_keys=True),
                ),
            )
            self._connection.commit()

    def index_scenes(self, scenes: Sequence[EOScene]) -> None:
        for scene in scenes:
            self.index_scene(scene)

    def query_scenes(
        self,
        roi: Sequence[float] | None = None,
        platform: str | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        max_cloud_cover: float | None = None,
        required_assets: Sequence[str] | None = None,
    ) -> list[EOScene]:
        conditions: list[str] = []
        parameters: list[object] = []
        if roi is not None:
            min_x, min_y, max_x, max_y = validate_bbox(roi)
            conditions.extend(["max_x >= ?", "min_x <= ?", "max_y >= ?", "min_y <= ?"])
            parameters.extend([min_x, max_x, min_y, max_y])
        if platform is not None:
            conditions.append("platform = ?")
            parameters.append(platform)
        if start_time is not None:
            conditions.append("acquired_at >= ?")
            parameters.append(start_time.isoformat())
        if end_time is not None:
            conditions.append("acquired_at <= ?")
            parameters.append(end_time.isoformat())
        if max_cloud_cover is not None:
            if not 0 <= max_cloud_cover <= 100:
                raise ValueError("max_cloud_cover must be between 0 and 100")
            conditions.append("cloud_cover <= ?")
            parameters.append(max_cloud_cover)
        sql = "SELECT * FROM scenes"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        sql += " ORDER BY acquired_at, scene_id"
        with self._lock:
            rows = self._connection.execute(sql, parameters).fetchall()
        scenes = [self._row_to_scene(row) for row in rows]
        if roi is not None:
            scenes = [scene for scene in scenes if scene_intersects_roi(scene, roi)]
        if required_assets:
            required = tuple(required_assets)
            scenes = [scene for scene in scenes if all(asset in scene.assets for asset in required)]
        return scenes

    def scene_ids(self) -> set[str]:
        with self._lock:
            rows = self._connection.execute("SELECT scene_id FROM scenes").fetchall()
        return {row["scene_id"] for row in rows}

    def prune_older_than(self, cutoff: datetime) -> int:
        """Delete scenes acquired before cutoff and return the number removed."""
        with self._lock:
            cursor = self._connection.execute(
                "DELETE FROM scenes WHERE acquired_at < ?", (cutoff.isoformat(),)
            )
            self._connection.commit()
            return cursor.rowcount

    def vacuum(self) -> None:
        """Checkpoint WAL, verify integrity, and reclaim unused database pages."""
        with self._lock:
            integrity = self._connection.execute("PRAGMA integrity_check").fetchone()[0]
            if integrity != "ok":
                raise sqlite3.DatabaseError(f"catalog integrity check failed: {integrity}")
            self._connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")
            self._connection.execute("VACUUM")

    def _row_to_scene(self, row: sqlite3.Row) -> EOScene:
        footprint = tuple(tuple(point) for point in json.loads(row["footprint_json"]))
        return EOScene(
            row["scene_id"],
            row["platform"],
            datetime.fromisoformat(row["acquired_at"]),
            row["cloud_cover"],
            footprint,
            (row["min_x"], row["min_y"], row["max_x"], row["max_y"]),
            row["epsg"],
            json.loads(row["assets_json"]),
        )
