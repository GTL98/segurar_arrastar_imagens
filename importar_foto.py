import cv2
class ImportarFoto:
    def __init__(self, caminho, posicao_original, tipo_foto):
        self.caminho = caminho
        self.posicao_original = posicao_original
        self.tipo_foto = tipo_foto
        
        if self.tipo_foto == 'png':
            self.imagem = cv2.imread(self.caminho, cv2.IMREAD_UNCHANGED)
        else:
            self.imagem = cv2.imread(self.caminho)
        
        self.tamanho = self.imagem.shape[:2]
        
    def atualizar(self, cursor):
        ox, oy = self.posicao_original
        altura_foto, largura_foto = self.tamanho
        
        if ox < cursor[0] < ox + largura_foto and oy < cursor[1] < oy + altura_foto:
            self.posicao_original = cursor[0] - largura_foto // 2, cursor[1] - altura_foto // 2