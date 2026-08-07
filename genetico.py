import numpy

class Cromossomo:
    def __init__(self, mass : float, potencia : float, cd : float, cl : float, A : float, mu : float, crr : float) -> None:
        self.mass = mass
        self.potencia = potencia
        self.cd = cd
        self.cl = cl
        self.cl = A
        self.mu = mu
        self.crr = crr
        
class AlgoritmoGenetico:
    def __init__(self, num_geracoes : int, taxa_cruzamento : float, taxa_mutacao : float, tam_populacao : int) -> None:
        self.num_geracoes = num_geracoes
        self.taxa_cruzamento = taxa_cruzamento
        self.taxa_mutacao = taxa_mutacao
        self.tam_populacao = tam_populacao
        self.populacao = []
    pass
    
    def iniciarPopulacao(self):
        