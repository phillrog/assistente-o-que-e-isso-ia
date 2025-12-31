import numpy as np
import os
import urllib.request
from ultralytics import YOLO

class YoloService:
    def __init__(self, caminho_modelo, url_download=None):
        self.caminho_modelo = caminho_modelo
        self.url_download = url_download
        self._assegurar_modelo()
        self.model = YOLO(self.caminho_modelo)
        
    def _assegurar_modelo(self):
        if not os.path.exists(self.caminho_modelo) and self.url_download:
            diretorio = os.path.dirname(self.caminho_modelo)
            if not os.path.exists(diretorio):
                os.makedirs(diretorio)
            
            urllib.request.urlretrieve(self.url_download, self.caminho_modelo)

    def validar_privacidade(self, imagem_pil):
        if self.model_yolo_face is None: 
            return False
            
        # Converte a imagem para o formato que o YOLO entende
        img_array = np.array(imagem_pil.convert('RGB'))
        
        # Executa a predição
        results = self.model_yolo_face.predict(img_array, conf=0.8, verbose=False)
        
        # Retorna True se encontrar qualquer caixa de detecção (rosto)
        return any(len(r.boxes) > 0 for r in results)