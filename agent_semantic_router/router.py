"""Fast TF-IDF cosine semantic router for LLM prompts."""
import math
import re
from typing import Dict, List, Tuple


class SemanticRouter:
    def __init__(self, confidence_threshold: float = 0.25):
        self._routes: Dict[str, List[str]] = {}
        self.threshold = confidence_threshold

    def add_route(self, route_name: str, sample_prompts: List[str]):
        self._routes[route_name] = sample_prompts

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\w+", text.lower())

    def _get_vector(self, tokens: List[str]) -> Dict[str, float]:
        counts: Dict[str, int] = {}
        for t in tokens:
            counts[t] = counts.get(t, 0) + 1
        length = math.sqrt(sum(c * c for c in counts.values())) or 1.0
        return {t: c / length for t, c in counts.items()}

    def _cosine(self, v1: Dict[str, float], v2: Dict[str, float]) -> float:
        score = 0.0
        for t, val in v1.items():
            if t in v2:
                score += val * v2[t]
        return score

    def route(self, query: str, default_route: str = "general") -> Tuple[str, float]:
        q_tokens = self._tokenize(query)
        if not q_tokens:
            return default_route, 0.0

        q_vec = self._get_vector(q_tokens)
        best_route = default_route
        best_score = 0.0

        for r_name, samples in self._routes.items():
            for sample in samples:
                s_tokens = self._tokenize(sample)
                s_vec = self._get_vector(s_tokens)
                sim = self._cosine(q_vec, s_vec)
                if sim > best_score:
                    best_score = sim
                    best_route = r_name

        if best_score < self.threshold:
            return default_route, best_score
        return best_route, best_score
