import math
from typing import List, Dict


def cosine_similarity(vec1, vec2):
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot / (norm1 * norm2)


class InMemoryVectorStore:
    def __init__(self):
        self.vectors: List[List[float]] = []
        self.metadata: List[Dict] = []

    def add(self, embedding: List[float], data: Dict):
        self.vectors.append(embedding)
        self.metadata.append(data)

    def search(self, query_embedding: List[float], top_k: int = 3):
        scores = []

        for i, vec in enumerate(self.vectors):
            score = cosine_similarity(query_embedding, vec)
            scores.append((score, self.metadata[i]))

        scores.sort(key=lambda x: x[0], reverse=True)

        return [item[1] for item in scores[:top_k]]