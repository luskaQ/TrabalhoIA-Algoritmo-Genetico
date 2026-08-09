import numpy
import fitnessMonza
import random

class Cromossomo:
    def __init__(self, mass : float, potencia : float, cd : float, cl : float, A : float, mu : float, crr : float) -> None:
        self.mass = mass
        self.potencia = potencia #
        self.cd = cd # arrasto aerodinamico
        self.cl = cl #coeficiente de lift, aqui funciona como um coeficiente de downforce
        self.A = A #area frontal do veiculo
        self.mu = mu #coeficiente de atrito dos pneus com o solo
        self.crr = crr #resistencia ao rolamento dos pneus ao solo
        self.fitness = -1
        
    def setFitness(self, fitness):
        self.fitness = fitness
        
        
class AlgoritmoGenetico:
    def __init__(self, num_geracoes : int, taxa_cruzamento : float, taxa_mutacao : float, magnitude_mutacao : float, tam_populacao : int) -> None:
        self.num_geracoes = num_geracoes
        self.taxa_cruzamento = taxa_cruzamento
        self.taxa_mutacao = taxa_mutacao
        self.tam_populacao = tam_populacao
        self.magnitude_mutacao = magnitude_mutacao
        self.populacao = []
    pass
    
    def geraCromossomoAleatorio(self):
        massa = round(random.uniform(768.0, 880.00), 4)
        potencia = round(random.uniform(670000.0, 780000.00), 4) #em W
        cd = round(random.uniform(0.7, 1.1), 4)
        cl = round(random.uniform(2.5, 4.5), 4)
        A = round(random.uniform(1.4, 1.6), 4) #metros quadrados
        mu = round(random.uniform(1.5, 1.8), 4)
        crr = round(random.uniform(0.015, 0.025), 5)
        cromossomo = Cromossomo(massa, potencia, cd, cl, A, mu, crr)
        self.calcularFitnessIndividuo(cromossomo, massa, potencia, cd, cl, A, mu, crr)

        return cromossomo

    """ 
        print(cromossomo.mass)
        print(cromossomo.potencia)
        print(cromossomo.cd)
        print(cromossomo.cl)
        print(cromossomo.A)
        print(cromossomo.mu)
        print(cromossomo.crr) 
        print(f"Lap time: {cromossomo.fitness}") 
    """
    def limitarGene(self, valor, minimo, maximo):
        if valor > maximo:
            return maximo
        elif valor < minimo:
            return minimo
        return valor
        
    def iniciarPopulacao(self):
        for i in range(self.tam_populacao):
            self.populacao.append(self.geraCromossomoAleatorio())
        pass
        
    def mutarCromossomo(self, cromossomo: Cromossomo):
        gene_mutado = random.randint(1, 7)

        if gene_mutado == 1:
            delta = random.uniform(
                -self.magnitude_mutacao * abs(cromossomo.mass),
                self.magnitude_mutacao * abs(cromossomo.mass)
            )
            cromossomo.mass = self.limitarGene(
                cromossomo.mass + delta,
                768.0,
                880.0
            )

        elif gene_mutado == 2:
            delta = random.uniform(
                -self.magnitude_mutacao * abs(cromossomo.potencia),
                self.magnitude_mutacao * abs(cromossomo.potencia)
            )
            cromossomo.potencia = self.limitarGene(
                cromossomo.potencia + delta,
                670000.0,
                780000.0
            )

        elif gene_mutado == 3:
            delta = random.uniform(
                -self.magnitude_mutacao * abs(cromossomo.cd),
                self.magnitude_mutacao * abs(cromossomo.cd)
            )
            cromossomo.cd = self.limitarGene(
                cromossomo.cd + delta,
                0.7,
                1.1
            )

        elif gene_mutado == 4:
            delta = random.uniform(
                -self.magnitude_mutacao * abs(cromossomo.cl),
                self.magnitude_mutacao * abs(cromossomo.cl)
            )
            cromossomo.cl = self.limitarGene(
                cromossomo.cl + delta,
                2.5,
                4.5
            )

        elif gene_mutado == 5:
            delta = random.uniform(
                -self.magnitude_mutacao * abs(cromossomo.A),
                self.magnitude_mutacao * abs(cromossomo.A)
            )
            cromossomo.A = self.limitarGene(
                cromossomo.A + delta,
                1.4,
                1.6
            )

        elif gene_mutado == 6:
            delta = random.uniform(
                -self.magnitude_mutacao * abs(cromossomo.mu),
                self.magnitude_mutacao * abs(cromossomo.mu)
            )
            cromossomo.mu = self.limitarGene(
                cromossomo.mu + delta,
                1.5,
                1.8
            )

        elif gene_mutado == 7:
            delta = random.uniform(
                -self.magnitude_mutacao * abs(cromossomo.crr),
                self.magnitude_mutacao * abs(cromossomo.crr)
            )
            cromossomo.crr = self.limitarGene(
                cromossomo.crr + delta,
                0.015,
                0.025
            )
        self.calcularFitnessIndividuo(
            cromossomo,
            cromossomo.mass,
            cromossomo.potencia,
            cromossomo.cd,
            cromossomo.cl,
            cromossomo.A,
            cromossomo.mu,
            cromossomo.crr
        )
    
    def mutarPopulacao(self):
        num_mutacoes = int(self.tam_populacao * self.taxa_mutacao)
        for i in range(num_mutacoes):
            idx = random.randint(0, self.tam_populacao - 1)
            self.mutarCromossomo(self.populacao[idx]) #mesmo cromossomo pode ser mutado 2x
        pass
    
    def cruzarPopulacao(self):
        pass
    
    def selecionarPopulacao(self):
        pass
    
    def calcularFitnessIndividuo(self, cromossomo,  massa, potencia, cd, cl, A, mu, crr):
        fitness = fitnessMonza.lap_time_simulator(massa, potencia, cd, cl, A, mu, crr) #tempo teorico do carro em uma volta de monza
        cromossomo.setFitness(fitness)
        pass
    
    def calcularFitnessPopulação(self):
        pass

alg = AlgoritmoGenetico(0,0,0,0,0)
alg.geraCromossomoAleatorio()
