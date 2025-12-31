import base64

def preparar_imagem_base64(imagem_arquivo):
    """Converte o arquivo do Streamlit para string base64 para a API do Gemini."""
    return f"data:image/jpeg;base64,{base64.b64encode(imagem_arquivo.getvalue()).decode('utf-8')}"