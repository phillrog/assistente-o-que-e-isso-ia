import base64
from io import BytesIO
from gtts import gTTS

class VozGttsService:
    @staticmethod
    def gerar_audio_base64(texto, lang_code):
        """Sintetiza voz e retorna em base64."""
        try:
            tts = gTTS(text=texto.lower(), lang=lang_code, slow=False)
            fp = BytesIO()
            tts.write_to_fp(fp)
            return base64.b64encode(fp.getvalue()).decode()
        except Exception:
            return None