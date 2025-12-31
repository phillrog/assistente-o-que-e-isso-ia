import numpy as np
import os
import urllib.request
from ultralytics import YOLO

class YoloService:
    def __init__(self, caminho_modelo, url_download=None):
        self.caminho_modelo = caminho_modelo
        self.url_download = url_download
        self._assegurar_modelo()
        try:
            self.model_yolo_face = YOLO(self.caminho_modelo)
        except Exception as e:
            print(f"Erro ao carregar o modelo YOLO: {e}")
            self.model_yolo_face = None
        
    def _assegurar_modelo(self):
        # Verifica se o arquivo físico existe no disco
        if not os.path.exists(self.caminho_modelo):
            if self.url_download:
                diretorio = os.path.dirname(self.caminho_modelo)
                if diretorio and not os.path.exists(diretorio):
                    os.makedirs(diretorio, exist_ok=True)
                
                # O download acontece aqui
                print(f"Iniciando download do modelo para: {self.caminho_modelo}")
                urllib.request.urlretrieve(self.url_download, self.caminho_modelo)
                print("Download concluído!")
            else:
                print("Erro: Arquivo não existe e nenhuma URL de download foi fornecida.")
            

    def validar_privacidade(self, imagem_pil):
        if self.model_yolo_face is None: 
            return False
            
        # Converte a imagem para o formato que o YOLO entende
        img_array = np.array(imagem_pil.convert('RGB'))
        
        # Executa a predição
        results = self.model_yolo_face.predict(img_array, conf=0.8, verbose=False)
        
        # Retorna True se encontrar qualquer caixa de detecção (rosto)
        return any(len(r.boxes) > 0 for r in results)