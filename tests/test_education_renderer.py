import pytest

pytest.importorskip("pymupdf")
pytest.importorskip("docx")

from docs.education.render_book import latex_to_text


def test_fraction_parser_accepts_whitespace_between_groups() -> None:
    result = latex_to_text(
        r"\frac{2\,\mathrm{Precision}_{ice}\,\mathrm{Recall}_{ice}} "
        r"{\mathrm{Precision}_{ice}+\mathrm{Recall}_{ice}}"
    )

    assert result == "(2 Precision_(ice) Recall_(ice))/(Precision_(ice)+Recall_(ice))"


def test_common_fraction_and_minimum_notation_are_preserved() -> None:
    assert latex_to_text(r"-\tfrac12(x+y)") == "-(1)/(2)(x+y)"
    assert latex_to_text(r"\tau_n = \min(D,\ d\,2^n)") == "τₙ = min(D, d 2ⁿ)"


def test_mean_gamma_and_matrix_notation_are_preserved() -> None:
    assert latex_to_text(r"\bar{x}=\frac{1}{n}\sum_{i=1}^{n}x_i") == ("x̄ = (1)/(n)Σ(i = 1 to n)xᵢ")
    assert latex_to_text(r"\gamma^0") == "γ⁰"
    assert latex_to_text(r"\begin{bmatrix}4&0\\0&4\end{bmatrix}") == ("[[4, 0], [0, 4]]")
    assert (
        latex_to_text(r"\hat{y} = \begin{cases}1, & s(x)>t\\0, & \text{otherwise}\end{cases}")
        == "ŷ = cases: 1, s(x)>t; 0, otherwise"
    )


def test_unsupported_math_command_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unsupported mathematical command: \\\\unknown"):
        latex_to_text(r"\unknown{x}")
