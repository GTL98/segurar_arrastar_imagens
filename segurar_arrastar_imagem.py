# 1. Importar as bibliotecas
import os
import cv2
import cvzone
from importar_foto import ImportarFoto
from cvzone.HandTrackingModule import HandDetector

# 2. Carregar o módulo de detecção
detector = HandDetector(maxHands=1, detectionCon=0.8, minTrackCon=0.8)

# 3. Definir o tamanho da tela
largura_tela = 1280
altura_tela = 720

# Pegar as fotos que usaremos
#foto = cv2.imread('imagens_jpg/1.jpg')
#foto = cv2.imread('imagens_png/1.png', cv2.IMREAD_UNCHANGED)
# Ponto de origem das fotos
#ox, oy = 200, 200

# 4. Pegar as fotos que usaremos
caminho = 'imagens_png'
minha_lista = os.listdir(caminho)
lista_fotos = []
for x, caminho_foto in enumerate(minha_lista):
    if 'png' in caminho_foto:
        tipo_foto = 'png'
    else:
        tipo_foto = 'jpg'
    lista_fotos.append(ImportarFoto(f'{caminho}/{caminho_foto}', [50+x*300, 50], tipo_foto))

# 5. Captura de vídeo
cap = cv2.VideoCapture(0)
cap.set(3, largura_tela)
cap.set(4, altura_tela)

while True:
    # Detectar as mãos
    sucesso, imagem = cap.read()
    imagem = cv2.flip(imagem, 1)
    maos, imagem = detector.findHands(imagem, flipType=False)
    
    # Extrair as informações das mãos
    if maos:
        lista_landmark = maos[0]['lmList']
        # Descobrir a distância entre a ponta do dedo indicador e do dedo médio
        # Checar se foi clicado
        comprimento, info, imagem = detector.findDistance(lista_landmark[8], lista_landmark[12], imagem)
        if comprimento < 20:
            cursor = lista_landmark[8]  # ponta do dedo indicador
            # Checar a região do clique
            for foto in lista_fotos:
                foto.atualizar(cursor)
    
    try:
        for foto in lista_fotos:
            # Manipular as fotos na tela (JPG)
            altura_foto, largura_foto = foto.tamanho
            ox, oy = foto.posicao_original
            if foto.tipo_foto == 'png':
                # Manipular as fotos na tela (PNG)
                imagem = cvzone.overlayPNG(imagem, foto.imagem, [ox, oy])
            else:
                imagem[oy: oy+altura_foto, ox: ox+largura_foto] = foto.imagem   
    except:
        pass
    
    # Mostrar a imagem na tela
    cv2.imshow('Segurar e Arrastar com Imagens', imagem)
    
    # Terminar o loop
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break
        
# 6. Fechar a tela de captura
cap.release()
cv2.destroyAllWindows()