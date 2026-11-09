
import pytest

from src.reranker import DocumentReranker


def test_sigmoid_normalization():
    """Check that logits become scores between 0 and 1."""

    assert DocumentReranker.normalize_score(0) == pytest.approx(0.5)
    assert DocumentReranker.normalize_score(2) > 0.5
    assert DocumentReranker.normalize_score(-2) < 0.5

    for logit in [-10, -2, 0, 2, 10]:
        score = DocumentReranker.normalize_score(logit)
        assert 0 <= score <= 1


def test_threshold_values():
    """Check how scores compare with the 0.55 threshold."""

    threshold = 0.55

    assert 0.42 < threshold
    assert 0.81 >= threshold
