from fastembed import TextEmbedding

_model = TextEmbedding()

def get_embedding(text: str):
    return list(_model.embed([text]))[0].tolist()