import streamlit as st
import os
from pathlib import Path
import base64
from PIL import Image
import json
from utils.image_helper import preparar_imagem_base64
from services.yolo_service import YoloService
from services.voz_gtts_service import VozGttsService
from services.ai_lang_gemini_service import AILangGemini

# ==========================================
# 1. CONFIGURAÇÃO E ESTILO
# ==========================================
st.set_page_config(
    page_title="O que é isso IA ?", 
    layout="wide", 
    page_icon="🗣️"
)

# INICIALIZAÇÃO OBRIGATÓRIA (Evita KeyError)
if 'reset_counter' not in st.session_state:
    st.session_state['reset_counter'] = 0

def carregar_estilo():
    caminho_css = Path(__file__).parent / "assets" / "style.css"
    
    if caminho_css.exists():
        with open(caminho_css, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"Aviso: Arquivo de estilo não encontrado em {caminho_css}")
        
st.set_page_config(page_title="O que é isso IA ?", layout="wide")
carregar_estilo()

# ==========================================
# 2. INICIALIZAÇÃO DE SERVIÇOS
# ==========================================
@st.cache_resource
def iniciar_servico_visao():
    url = "https://github.com/lindevs/yolov8-face/releases/download/1.0.1/yolov8x-face-lindevs.pt"
    diretorio_base = os.path.dirname(os.path.abspath(__file__))
    caminho_modelo = os.path.join(diretorio_base, 'pre-trained-models', 'yolo', 'yolov8x-face-lindevs.pt')

    return YoloService(caminho_modelo, url_download=url)

yolo_service = iniciar_servico_visao()

# Constantes de Interface
IDIOMAS = {
    "Português (BR)": "pt-br", 
    "English (US)": "en", 
    "Español": "es", 
    "Deutsch (Alemão)": "de", 
    "Русский (Russo)": "ru"
}
LABELS_ENCONTREI = {"pt-br": "Eu encontrei:", "en": "I found:", "es": "He encontrado:", "de": "Ich habe gefunden:", "ru": "Я нашел:"}
LABELS_SABIA = {"pt-br": "Você sabia?", "en": "Did you know?", "es": "¿Sabías que?", "de": "Wussten Sie schon?", "ru": "Вы знали?"}

# ==========================================
# 3. SIDEBAR (CONFIGURAÇÕES)
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3468/3468094.png", width=80)
    st.title("Configurações")
    
    api_key = st.text_input("Sua API Key", type="password", help="Chave do Google AI Studio.")
    
    modelos_disponiveis = {
        "Gemini 2.0 Flash": "gemini-2.0-flash",
        "Gemini 3 Flash (Preview)": "gemini-3-flash-preview",
    }
    
    modelo_selecionado = st.selectbox(
        "Escolha o Cérebro da IA (LLM):",
        options=list(modelos_disponiveis.keys())
    )

    idioma_nome = st.selectbox("Idioma da Descoberta:", options=list(IDIOMAS.keys()))
    lang_code = IDIOMAS[idioma_nome]
    
    metodo_entrada = st.radio("Entrada:", ("📁 Arquivo", "📷 Câmera"))   

    # RESET COMPLETO E SEGURO
    if st.button("🗑️ Limpar Sessão", type="secondary"):
        proximo_reset = st.session_state.get('reset_counter', 0) + 1
        st.session_state.clear()
        st.session_state['reset_counter'] = proximo_reset
        st.rerun()
        
    st.markdown("---")
    st.caption('Para Sarinha')

# ==========================================
# 4. CABEÇALHO
# ==========================================
st.markdown(f"""
<div class="header-container">
    <div class="main-title"><img src="https://cdn-icons-png.flaticon.com/512/3468/3468094.png" alt="0" style="width: 64px; max-width: 100%;"> O que é isso IA ?</div>
    <div style="color: #718096; font-size: 18px;">Exploração Multilíngue com Inteligência Artificial 🌍</div>
</div>

""", unsafe_allow_html=True)

# ==========================================
# 5. LÓGICA PRINCIPAL
# ==========================================
arquivo_imagem = None

if api_key:
    # CHAVES DINÂMICAS PARA RESET FÍSICO
    versao = st.session_state.get('reset_counter', 0)
    
    if metodo_entrada == "📁 Arquivo":
        arquivo_imagem = st.file_uploader("Subir foto", type=["jpg", "png", "jpeg"], key=f"up_{versao}")
    else:
        arquivo_imagem = st.camera_input("Tirar foto", key=f"cam_{versao}")
    
    if arquivo_imagem:
        id_foto = f"{getattr(arquivo_imagem, 'name', str(arquivo_imagem.size))}_{lang_code}_{versao}"
        
        if st.session_state.get('id_foto_anterior') != id_foto:
            st.session_state.update({
                'palavra': None, 'curiosidade': None, 'audio': None, 
                'id_foto_anterior': id_foto, 'executar_scroll': False
            })

        img_original = Image.open(arquivo_imagem)
        
        # Validação de Privacidade
        if yolo_service and yolo_service.validar_privacidade(img_original):
            st.error("🚫 Ops! Identificamos um rosto. Por segurança, aponte para um objeto.")
        else:
            if st.session_state.get('palavra') is None:
                with st.spinner(f"Analisando em {idioma_nome}... ✨"):

                    try:
                        ai_engine = AILangGemini(api_key, modelos_disponiveis[modelo_selecionado])
                        img_b64 = preparar_imagem_base64(arquivo_imagem)
                        
                        # Recebe o texto com as tags <p> e <c>
                        resposta = str(ai_engine.analisar_objeto(img_b64, idioma_nome))
                        
                        # Extração inteligente via fatiamento de string (sem erros de lista!)
                        def extrair(tag, texto):
                            try:
                                inicio = texto.find(f"<{tag}>") + len(tag) + 2
                                fim = texto.find(f"</{tag}>")
                                return texto[inicio:fim].strip()
                            except:
                                return ""

                        palavra = extrair("p", resposta) or "Identificado"
                        fonetica = extrair("f", resposta) or "" # Captura a prática de pronúncia
                        curiosidade = extrair("c", resposta) or "Curiosidade não disponível."
                        traducao = extrair("t", resposta) # Captura a tradução
                        
                        st.session_state.update({
                            'palavra': palavra,
                            'fonetica': fonetica, 
                            'curiosidade': curiosidade,
                            'traducao': traducao, 
                            'audio': VozGttsService.gerar_audio_base64(palavra, lang_code)
                        })
                        st.balloons()

                    except Exception as e:
                        st.error(f"Erro na análise: {e}")

            # --- EXIBIÇÃO DOS RESULTADOS ---
            if st.session_state.get('palavra'):
                col1, col2 = st.columns([1, 1.2])
                
                with col1:                
                    st.markdown('<div class="img-fixa">', unsafe_allow_html=True)
                    st.image(img_original, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                with col2:
                    st.markdown(f"""
                        <div class="magic-card" style="min-height: 350px; display: flex; flex-direction: column; justify-content: center;">
                            <div style="font-size: 25px; color: #718096; margin-bottom: 10px;">{LABELS_ENCONTREI.get(lang_code)}</div>
                            <div style="font-size: 4.5rem; color: #4A90E2; font-weight: 900; line-height: 1.1;">{st.session_state['palavra']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.session_state['audio']:
                        st.audio(base64.b64decode(st.session_state['audio']), format="audio/mp3")

                if st.session_state.get('fonetica'):
                    st.markdown(f"""
                        <div style="background-color: #f0f7ff; padding: 20px; border-radius: 20px; border: 2px dashed #4A90E2; margin-top: 25px; box-shadow: 0 4px 10px rgba(74,144,226,0.1);">
                            <b style="color: #2B6CB0; font-size: 18px;">🗣️ Pratique a Pronúncia:</b>
                            <p style="color: #2D3748; font-size: 24px; font-weight: bold; margin-top: 10px; letter-spacing: 1px;">
                                {st.session_state['fonetica']}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown(f"""
                    <div style="background-color: white; padding: 25px; border-radius: 20px; border-left: 10px solid #4A90E2; margin-top: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                        <b style="color: #2B6CB0; font-size: 22px;">💡 {LABELS_SABIA.get(lang_code)}</b>
                        <p style="color: #2D3748; font-size: 18px; line-height: 1.6; margin-top: 10px;">{st.session_state['curiosidade']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # EXIBIÇÃO DA TRADUÇÃO (Apenas se houver tradução e não for PT-BR)
                if lang_code != "pt-br" and st.session_state.get('traducao'):
                    st.markdown(f"""
                    <div style="background-color: white; padding: 25px; border-radius: 20px; border-left: 10px solid #ececec; margin-top: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                        <b style="color: #2B6CB0; font-size: 22px;">🔑 Tradução </b>
                        <p style="color: #2D3748; font-size: 18px; line-height: 1.6; margin-top: 10px;">{st.session_state['traducao']}</p>
                    </div>
                """, unsafe_allow_html=True)
                    

                if st.session_state.get('last_played') != id_foto:
                    st.markdown(f'<audio autoplay src="data:audio/mp3;base64,{st.session_state["audio"]}"></audio>', unsafe_allow_html=True)
                    st.session_state['last_played'] = id_foto

else:
    # REINTEGRANDO MENSAGENS DE BOAS-VINDAS ORIGINAIS
    st.warning("⚠️ **Acesso Bloqueado:** Insira sua **API Key** no menu lateral para começar.")
    
    st.markdown("""
    <div style="text-align: center; ">
        <img src="https://cdn-icons-png.flaticon.com/512/3062/3062063.png" width="150">
        <h2 style="color: #4A90E2;">Bem-vindo à Aventura!</h2>
        <p style="font-size: 18px; color: #718096;">Escolha um idioma e insira a sua API Key para começar.</p>
    </div>
    """, unsafe_allow_html=True)