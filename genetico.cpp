#include <iostream>
#include <vector>

// Hiperparametros
#define NUM_DE_GERACOES 5000
#define TAM_POPULACAO 100
#define TAXA_CRUZAMENTO 0.1
#define TAXA_MUTACAO 0.1

using namespace std;

class AlgoritmoGenetico
{
public:
    void mutarCromossomo();

    void mutarPopulacao();

    void cruzarCromossomos();

    void cruzarPopulacao();

    void calcularFitnessCromossomo();

private:
    struct cromossomo
    {
        double velocidade_media_retas; //placeholder
        double fitness;
    };
    vector<cromossomo>populacao;
};