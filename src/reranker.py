
import math

from sentence_transformers import CrossEncoder


class DocumentReranker:
    def __init__(
        self,
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2",
        threshold=0.55,
    ):
        self.model = CrossEncoder(model_name)
        self.threshold = threshold

    @staticmethod
    def normalize_score(logit: float) -> float:
        """Convert a raw model score to a value between 0 and 1."""
        if logit >= 0:
            return 1.0 / (1.0 + math.exp(-logit))

        exp_value = math.exp(logit)
        return exp_value / (1.0 + exp_value)

    def rerank(self, query: str, candidates: list, top_k=5):
        """Score candidates and keep the most relevant chunks."""

        if not candidates or not query.strip():
            return [], 0.0, "LOW_CONFIDENCE"

        pairs = [
            (query, candidate["content"])
            for candidate in candidates
        ]

        raw_scores = self.model.predict(pairs)

        ranked = []

        for candidate, raw_score in zip(candidates, raw_scores):
            item = candidate.copy()
            item["rerank_score"] = float(raw_score)
            item["confidence"] = self.normalize_score(
                float(raw_score)
            )
            ranked.append(item)

        ranked.sort(
            key=lambda item: item["rerank_score"],
            reverse=True,
        )

        top_results = ranked[:top_k]
        confidence = top_results[0]["confidence"]

        status = (
            "HIGH_CONFIDENCE"
            if confidence >= self.threshold
            else "LOW_CONFIDENCE"
        )

        return top_results, confidence, status
