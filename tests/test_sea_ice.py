import pytest

np = pytest.importorskip("numpy")

from kvarken_eo.sea_ice import (  # noqa: E402
    agreement_metrics,
    buffered_water,
    fit_discriminant,
    optical_reference,
    power_to_db,
    predict_discriminant,
    spatial_partition,
)


def test_linear_power_to_db_excludes_invalid_values():
    result = power_to_db(np.array([1, 0.1, 0.01, 0, -32768, np.nan]))
    np.testing.assert_allclose(result[:3], [0, -10, -20])
    assert np.isnan(result[3:]).all()


def test_water_buffer_excludes_coast_invalid_data_and_image_boundary():
    classes = np.full((9, 9), 80)
    classes[4, 4] = 10
    result = buffered_water(classes, 1)
    assert not result[0].any()
    assert not result[:, -1].any()
    assert not result[3:6, 3:6].any()
    assert result[1, 1]
    with pytest.raises(ValueError):
        buffered_water(classes, -1)


def test_optical_reference_is_conservative_and_abstains_on_clouds_and_thin_ice():
    green = np.array([0.3, 0.03, 0.3, 0.1, np.nan])
    nir = np.array([0.3, 0.02, 0.3, 0.05, 0.3])
    swir = np.array([0.05, 0.01, 0.05, 0.04, 0.05])
    scl = np.array([11, 6, 9, 6, 11])
    labels = optical_reference(green, nir, swir, scl)
    np.testing.assert_array_equal(labels, [1, 0, -1, -1, -1])


def test_discriminant_learns_both_features_and_predicts_separated_samples():
    features = np.array([[-25, -30], [-24, -32], [-23, -29], [-10, -15], [-9, -13], [-11, -16]])
    labels = np.array([0, 0, 0, 1, 1, 1])
    model = fit_discriminant(features, labels)
    np.testing.assert_array_equal(predict_discriminant(features, model), labels)
    with pytest.raises(ValueError, match="both"):
        fit_discriminant(features[:3], labels[:3])
    with pytest.raises(ValueError, match="finite"):
        fit_discriminant(np.full((6, 2), np.nan), labels)


def test_agreement_reports_actual_confusion_matrix_and_no_ground_truth_claim():
    result = agreement_metrics(np.array([0, 0, 1, 1, 1]), np.array([0, 1, 0, 1, 1]))
    assert result["confusion_matrix_reference_rows"] == [[1, 1], [1, 2]]
    assert result["sample_count"] == 5
    assert result["agreement"] == pytest.approx(0.6)
    assert result["balanced_agreement"] == pytest.approx((0.5 + 2 / 3) / 2)
    assert result["ice_precision"] == pytest.approx(2 / 3)
    assert result["ice_recall"] == pytest.approx(2 / 3)
    assert result["ice_f1"] == pytest.approx(2 / 3)
    single = agreement_metrics(np.array([0, 0]), np.array([0, 1]))
    assert single["confusion_matrix_reference_rows"] == [[1, 1], [0, 0]]
    assert single["agreement"] == 0.5
    assert single["balanced_agreement"] is None
    assert single["ice_recall"] is None


def test_spatial_split_separates_training_and_test_and_excludes_block_edges():
    training, test, blocks = spatial_partition((40, 40), block_pixels=10, gap_pixels=2)
    assert training.any() and test.any()
    assert not (training & test).any()
    assert not training[:2].any() and not test[:2].any()
    for block in np.unique(blocks):
        assert not (training[blocks == block].any() and test[blocks == block].any())


def test_scientific_calculations_reject_misaligned_grids():
    with pytest.raises(ValueError, match="shape"):
        optical_reference(np.zeros(3), np.zeros(4), np.zeros(3), np.zeros(3))
    with pytest.raises(ValueError, match="shape"):
        agreement_metrics(np.array([0, 1]), np.array([0, 0, 1]))
