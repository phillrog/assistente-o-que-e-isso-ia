[![Build - Assistente O Que é Isso IA ?](https://github.com/phillrog/assistente-o-que-e-isso-ia/actions/workflows/build-conda.yml/badge.svg)](https://github.com/phillrog/assistente-o-que-e-isso-ia/actions/workflows/build-conda.yml)  - [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://assistente-exploracao-divertida.streamlit.app)

---

🗣️ O Que é Isso IA? Exploração Divertida 🌍
=================================================

Este projeto é uma plataforma educativa interativa que utiliza Inteligência Artificial e Visão Computacional para transformar o ambiente ao redor em uma sala de aula de idiomas. O app permite identificar objetos, resolver fórmulas matemáticas e praticar a pronúncia em diversos idiomas de forma segura e divertida.

<img width="1918" height="981" alt="image" src="https://github.com/user-attachments/assets/eaef12c6-5f93-4c02-8970-ae1fb5c32f8c" />


🚀 O Propósito e Fluxo de Operação
----------------------------------

O diferencial deste aplicativo é o seu fluxo de processamento inteligente dividido em duas camadas:

1.  **Camada de Privacidade (Local):** Antes de qualquer dado sair do dispositivo, a imagem é analisada pelo modelo **YOLOv8** (`yolov8x-face-lindevs.pt`). Se um rosto humano for detectado, o processo é interrompido para garantir a privacidade do usuário.

2.  **Camada de Inteligência (Nuvem):** Caso a imagem seja validada, ela é convertida para `Base64` e enviada ao **Google Gemini**, que atua como um tutor multilíngue.

* * * * *

🛠️ Tecnologias e Ferramentas
-----------------------------

-   **[Streamlit](https://streamlit.io/):** Interface de usuário responsiva e dinâmica.

-   **[YOLOv8](https://github.com/lindevs/yolov8-face/releases):** Validação de privacidade local com o modelo especializado `yolov8x-face-lindevs.pt`.

-   **[Google Gemini (via LangChain)](https://ai.google.dev/):** Análise multimodal de imagens e geração de conteúdo educativo.

-   **[gTTS (Google Text-to-Speech)](https://pypi.org/project/gTTS/):** Síntese de voz para auxílio na audição e pronúncia.

-   **[PIL (Pillow)](https://www.google.com/search?q=https://python-pillow.org/):** Manipulação e tratamento de imagens.

* * * * *

📋 Protocolo de Comunicação (Tags Estruturadas)
-----------------------------------------------

Para garantir que a interface apresente os dados de forma impecável e sem erros de processamento de texto, a IA utiliza um sistema de tags obrigatórias:

-   `<p>`: **Palavra/Contexto** (Ex: "The Eiffel Tower" ou "Equação de Segundo Grau").

-   `<f>`: **Prática Fonética** (Divisão silábica e guia de pronúncia).

-   `<c>`: **Curiosidade** (Fato educativo no idioma selecionado).

-   `<t>`: **Tradução** (Tradução para Português-BR da curiosidade, quando o idioma alvo for estrangeiro).

* * * * *

🏗️ Estrutura do Projeto (SOLID)
--------------------------------

O software foi desenvolvido seguindo princípios de design limpo para garantir escalabilidade:

Plaintext

```
├── app.py                # Orquestrador da Interface Streamlit
├── services/             # Lógica de Negócio (YoloService, GeminiService, VozService)
├── utils/                # Auxiliares (Conversão de Imagem, Helpers)
├── assets/               # CSS personalizado e animações
└── pre-trained-models/   # Modelos YOLO para detecção local

Obs: O modelo deve ser baixado automaticamente ao iniciar a aplicação pois não é possível armazenar um arquivo tão grande neste respositório.
```

* * * * *

## Como rodar o projeto

### 1. Criar o Ambiente Virtual
Isso garante que as bibliotecas do projeto não conflitem com outras no seu computador.
```bash
python -m venv .venv
```

### 2. Ativar o Ambiente Virtual

No Windows:

```bash
.\.venv\Scripts\activate
```

No Linux/Mac:

```bash
source .venv/bin/activate
```

### 3. Instalar as Dependências
Instale todas as bibliotecas necessárias listadas no arquivo requirements.txt.

```bash
pip install -r requirements.txt
```

### 4. Executar a Aplicação
Inicie o servidor do Streamlit para abrir a interface no seu navegador.

```bash
python -m streamlit run app.py
```

### 5.  Insira sua **Google API Key** no menu lateral e comece a exploração!

A aplicação utiliza o modelo **Gemini 2.0 Flash** e **Gemini 3 Flash (Preview)**. Para obter sua chave gratuita, siga estes passos:

1.  Acesse o [Google AI Studio](https://aistudio.google.com/).

2.  Faça login com sua conta Google.

3.  No menu lateral, clique em **"Get API key"**.

4.  Clique no botão **"Create API key in new project"**.

5.  Copie a chave gerada e cole-a no campo correspondente na barra lateral da aplicação.
Obs: Cuidado com os limites


# ⚠️ Disclaimer (Aviso de Uso)
Esta é uma ferramenta baseada em Inteligência Artificial Experimental. As análises fornecidas são sugestões educativas. O processamento de dados segue rigorosos filtros de privacidade locais, mas recomenda-se que o usuário valide todas as informações e consulte as políticas de privacidade do provedor (Google Gemini).

# Resultado
Teste com upload

![assistente-exp-1](https://github.com/user-attachments/assets/2b0b8c49-3425-44f0-8c65-f91bcd7f43a0)


![assistente-exp-2](https://github.com/user-attachments/assets/0bcda7da-8ae4-4bca-9a2c-a65f24b23054)


Teste com a câmera

https://github.com/user-attachments/assets/f3f629cb-d3b8-440c-bf6f-9741b7b22b46


