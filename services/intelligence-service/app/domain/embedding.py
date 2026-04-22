from fastembed import TextEmbedding

_model = TextEmbedding()

def get_embedding(text: str):
    # 🔥 lightweight placeholder embedding
    return [hash(text) % 1000 / 1000.0]