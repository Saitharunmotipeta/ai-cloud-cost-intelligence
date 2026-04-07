from sentence_transformers import SentenceTransformer

# Load once (global singleton)
_model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text: str) -> list:
    return _model.encode(text).tolist()