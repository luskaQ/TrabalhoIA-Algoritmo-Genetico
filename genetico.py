import numpy
import fitnessMonza
import random
import copy
import json
import matplotlib.pyplot as plt

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

    def __repr__(self):
        return (
            f"Cromossomo("
            f"mass={self.mass:.2f}, "
            f"potencia={self.potencia:.2f}, "
            f"cd={self.cd:.4f}, "
            f"cl={self.cl:.4f}, "
            f"A={self.A:.4f}, "
            f"mu={self.mu:.4f}, "
            f"crr={self.crr:.5f}, "
            f"fitness={self.fitness:.4f}"
            f")\n"
        )
        
        
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
        #tipo_mutacao = random.randint(1,2)
        gene_mutado = random.randint(1, 6)
        delta = random.uniform(
            -self.magnitude_mutacao * abs(cromossomo.A),
            self.magnitude_mutacao * abs(cromossomo.A)    
        )
        cromossomo.A = self.limitarGene(                cromossomo.A + delta,
            1.4,
            1.6
        )
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
                -self.magnitude_mutacao * abs(cromossomo.mu),
                self.magnitude_mutacao * abs(cromossomo.mu)
            )
            cromossomo.mu = self.limitarGene(
                cromossomo.mu + delta,
                1.5,
                1.8
            )
        elif gene_mutado == 6:
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
            idx = random.randint(1, len(self.populacao) - 1)
            self.mutarCromossomo(self.populacao[idx]) #mesmo cromossomo pode ser mutado 2x
        pass
    
    def cruzarPopulacao(self):
        quantidade_cruzamento = int(self.tam_populacao * self.taxa_cruzamento)

        genes = [
            "mass",
            "potencia",
            "cd",
            "cl",
            "A",
            "mu",
            "crr"
        ]        

        for i in range (quantidade_cruzamento):
            gene_cruzado = random.randint(1, 7)
            idx_cromossomo1 = random.randint(0, self.tam_populacao-1)

            while True:
                idx_cromossomo2 = random.randint(0, self.tam_populacao-1)
                if idx_cromossomo1 != idx_cromossomo2:
                    break

            cromossomo1 = self.populacao[idx_cromossomo1]
            cromossomo2 = self.populacao[idx_cromossomo2]

            cromossomo_cruzado1 = copy.deepcopy(cromossomo1)
            cromossomo_cruzado2 = copy.deepcopy(cromossomo2)

            gene_cruzado = random.choice(genes)

            valor1 = getattr(cromossomo_cruzado1, gene_cruzado)
            valor2 = getattr(cromossomo_cruzado2, gene_cruzado)

            setattr(cromossomo_cruzado1, gene_cruzado, valor2)
            setattr(cromossomo_cruzado2, gene_cruzado, valor1)

            self.calcularFitnessIndividuo(
                cromossomo_cruzado1,
                cromossomo_cruzado1.mass,
                cromossomo_cruzado1.potencia,
                cromossomo_cruzado1.cd,
                cromossomo_cruzado1.cl,
                cromossomo_cruzado1.A,
                cromossomo_cruzado1.mu,
                cromossomo_cruzado1.crr
            )
            self.calcularFitnessIndividuo(
                cromossomo_cruzado2,
                cromossomo_cruzado2.mass,
                cromossomo_cruzado2.potencia,
                cromossomo_cruzado2.cd,
                cromossomo_cruzado2.cl,
                cromossomo_cruzado2.A,
                cromossomo_cruzado2.mu,
                cromossomo_cruzado2.crr
            )
            self.populacao.append(cromossomo_cruzado1)
            self.populacao.append(cromossomo_cruzado2)
        

    
    def selecionarPopulacao(self):
        self.populacao.sort(key=lambda cromossomo: cromossomo.fitness)
        self.populacao[:] = self.populacao[:self.tam_populacao]
    
    def calcularFitnessIndividuo(self, cromossomo,  massa, potencia, cd, cl, A, mu, crr):
        fitness = fitnessMonza.lap_time_simulator(massa, potencia, cd, cl, A, mu, crr) #tempo teorico do carro em uma volta de monza
        cromossomo.setFitness(fitness)
        pass
    
    def execAlg(self):
        fitness = []
        self.iniciarPopulacao()
        self.selecionarPopulacao()
        for i in range(self.num_geracoes):
            #print(i)
            self.cruzarPopulacao()
            self.mutarPopulacao()
            self.selecionarPopulacao()
            fitness.append((self.populacao[0].fitness, self.populacao[self.tam_populacao//2].fitness, self.populacao[self.tam_populacao - 1].fitness))
            print(f"Geração {i}", '-'*40)
            print(self.populacao[0])
            print(self.populacao[self.tam_populacao//2])
            print(self.populacao[self.tam_populacao - 1])
        return fitness

num_geracoes = 50
taxa_cruzamento = 0.3
taxa_mutacao = 0.3
magnitude_mutacao = 0.99
tam_populacao = 100

alg = AlgoritmoGenetico(
                        num_geracoes=num_geracoes,
                        taxa_cruzamento=taxa_cruzamento,
                        taxa_mutacao=taxa_mutacao,
                        magnitude_mutacao=magnitude_mutacao,
                        tam_populacao=tam_populacao
                    )
meus_fitness = alg.execAlg()

dicionario = {
    "numero_geracoes_max":num_geracoes,
    "num_epocas_rodadas_realmente":len(meus_fitness),
    "taxa_cruzamento":taxa_cruzamento,
    "taxa_mutacao":taxa_mutacao,
    "magnitude_mutacao":magnitude_mutacao,
    "tam_populacao":tam_populacao,
    "fitness_do_melhor_ultima_geracao":meus_fitness[len(meus_fitness)-1][0]
}

arquivo = "resultados.json"

try:
    with open(arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    dados = []

dados.append(dicionario)

with open(arquivo, "w", encoding="utf-8") as f:
    json.dump(dados, f, indent=4, ensure_ascii=False)
    
geracoes = range(1, len(meus_fitness) + 1)

melhores = [fitness[0] for fitness in meus_fitness]
medianos = [fitness[1] for fitness in meus_fitness]
piores = [fitness[2] for fitness in meus_fitness]

plt.plot(geracoes, melhores, label="Melhor")
plt.plot(geracoes, medianos, label="Mediano")
plt.plot(geracoes, piores, label="Pior")

plt.xlabel("Geração")
plt.ylabel("Fitness")
plt.title("Evolução do Fitness por Geração")
plt.legend()
plt.grid(True)
plt.savefig("img1.png")
