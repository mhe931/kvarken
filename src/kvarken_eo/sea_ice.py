"""Conservative optical-reference agreement for a single SAR sea-ice experiment."""

import numpy as np


def power_to_db(power: np.ndarray) -> np.ndarray:
    values = np.asarray(power, dtype=float)
    result = np.full(values.shape, np.nan)
    valid = np.isfinite(values) & (values > 0)
    result[valid] = 10 * np.log10(values[valid])
    return result


def buffered_water(classes: np.ndarray, radius_pixels: int) -> np.ndarray:
    if radius_pixels < 0:
        raise ValueError("radius_pixels must be non-negative")
    if classes.ndim != 2:
        raise ValueError("land-cover classes must be a two-dimensional grid")
    water = classes == 80
    padded = np.pad(water, radius_pixels, constant_values=False)
    result = np.ones_like(water)
    rows, columns = water.shape
    for row in range(2 * radius_pixels + 1):
        for column in range(2 * radius_pixels + 1):
            result &= padded[row : row + rows, column : column + columns]
    return result


def optical_reference(
    green: np.ndarray, nir: np.ndarray, swir: np.ndarray, scl: np.ndarray
) -> np.ndarray:
    if not (green.shape == nir.shape == swir.shape == scl.shape):
        raise ValueError("optical input shape mismatch")
    valid = np.isfinite(green) & np.isfinite(nir) & np.isfinite(swir)
    valid &= (green > 0) & (nir > 0) & (swir > 0)
    ndsi = np.divide(green - swir, green + swir, out=np.full(green.shape, np.nan), where=valid)
    labels = np.full(green.shape, -1, dtype=np.int8)
    labels[valid & (scl == 6) & (nir < 0.04) & (green < 0.10)] = 0
    labels[valid & (scl == 11) & (ndsi > 0.4) & (green > 0.15) & (nir > 0.10)] = 1
    return labels


def fit_discriminant(features: np.ndarray, labels: np.ndarray) -> dict:
    features = np.asarray(features, dtype=float)
    labels = np.asarray(labels)
    if features.ndim != 2 or features.shape[1] != 2 or labels.shape != (len(features),):
        raise ValueError("features/labels shape must be (n, 2) and (n,)")
    if not np.isfinite(features).all():
        raise ValueError("features must be finite")
    if not np.isin(labels, [0, 1]).all() or min(np.sum(labels == c) for c in (0, 1)) < 3:
        raise ValueError("both reference classes require at least three training samples")
    means = [features[labels == c].mean(axis=0) for c in (0, 1)]
    residuals = features - np.asarray(means)[labels]
    covariance = residuals.T @ residuals / (len(features) - 2)
    scale = max(float(np.trace(covariance) / 2), 1e-6)
    covariance = 0.95 * covariance + 0.05 * scale * np.eye(2)
    weights = np.linalg.solve(covariance, means[1] - means[0])
    intercept = -0.5 * float((means[1] + means[0]) @ weights)
    return {
        "weights": weights.tolist(),
        "intercept": intercept,
        "means_db": [mean.tolist() for mean in means],
        "covariance_db2": covariance.tolist(),
        "covariance_shrinkage": 0.05,
        "priors": [0.5, 0.5],
        "training_counts": [int(np.sum(labels == c)) for c in (0, 1)],
    }


def predict_discriminant(features: np.ndarray, model: dict, offset: float = 0) -> np.ndarray:
    scores = features @ np.asarray(model["weights"]) + model["intercept"]
    return (scores > offset).astype(np.int8)


def agreement_metrics(reference: np.ndarray, prediction: np.ndarray) -> dict:
    if reference.shape != prediction.shape:
        raise ValueError("reference and prediction shape mismatch")
    if not np.isin(reference, [0, 1]).all() or not np.isin(prediction, [0, 1]).all():
        raise ValueError("agreement requires binary labels, without nodata")
    if not reference.size:
        raise ValueError("agreement requires at least one reference sample")
    counts = [
        [int(np.sum((reference == actual) & (prediction == pred))) for pred in (0, 1)]
        for actual in (0, 1)
    ]
    tn, fp = counts[0]
    fn, tp = counts[1]
    return {
        "confusion_matrix_reference_rows": counts,
        "sample_count": int(reference.size),
        "agreement": (tn + tp) / reference.size,
        "balanced_agreement": (
            (tn / (tn + fp) + tp / (tp + fn)) / 2 if (tn + fp) and (tp + fn) else None
        ),
        "ice_precision": tp / (tp + fp) if tp + fp else None,
        "ice_recall": tp / (tp + fn) if tp + fn else None,
        "ice_f1": 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else None,
    }


def spatial_partition(
    shape: tuple[int, int], block_pixels: int = 100, gap_pixels: int = 10
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if block_pixels < 1 or gap_pixels < 0 or 2 * gap_pixels >= block_pixels:
        raise ValueError("block width must exceed twice the excluded edge gap")
    rows, columns = np.indices(shape)
    row_blocks, col_blocks = rows // block_pixels, columns // block_pixels
    blocks = row_blocks * (int(np.ceil(shape[1] / block_pixels))) + col_blocks
    inside = (
        (rows % block_pixels >= gap_pixels)
        & (rows % block_pixels < block_pixels - gap_pixels)
        & (columns % block_pixels >= gap_pixels)
        & (columns % block_pixels < block_pixels - gap_pixels)
    )
    training = inside & ((row_blocks + col_blocks) % 2 == 0)
    test = inside & ~training
    return training, test, blocks
