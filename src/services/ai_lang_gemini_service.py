from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

class AILangGemini:
    def __init__(self, api_key, model_name):
        self.llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)

    def analisar_objeto(self, imagem_b64, idioma_nome):
        prompt = (
            f"Analise a imagem e identifique o contexto principal para uma criança aprendendo {idioma_nome}. Caso for uma fórmula matemática resolva-a. "
            f"MANDATÓRIO: Todo o conteúdo das tags <p>, <f> e <c> deve estar escrito em {idioma_nome}. "
            "Sua resposta deve seguir OBRIGATORIAMENTE este formato, sem nenhum texto adicional:\n\n"
            "<p>Nome ou descrição do contexto principal</p>\n"
            "<f>Divida a palavra principal em sílabas usando '/' e para cada sílaba forneça um guia de pronúncia entre parênteses</f>\n"
            "<c>Uma curiosidade curta e educativa sobre ele.</c>\n"
            f"<t>Tradução para Português (Brasil) apenas do texto da tag <c>. Se o idioma selecionado já for Português, deixe esta tag vazia.</t>"
        )

        resposta = self.llm.invoke([HumanMessage(content=[
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": imagem_b64}}
        ])])
        return resposta.content