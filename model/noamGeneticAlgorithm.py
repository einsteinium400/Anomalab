import random
from model.KMeanClusterer import KMeansClusterer
import pygad as pygad

POPULATION_SIZE = 10
GENERATIONS = 10
EVALUATE_TIMES = 1

# Generate an initial population of solutions
def generate_population(maxDomainSize):
    population = []
    for i in range(POPULATION_SIZE):
        solution = []
        t = random.randint(1, maxDomainSize)
        t2 = random.randint(1, maxDomainSize)
        theta1 = min(t, t2)
        solution.append(theta1)
        theta2 = max(t, t2)
        solution.append(theta2)
        beta = random.uniform(0,1)
        solution.append(beta)
        gamma = random.uniform(0,1)
        solution.append(gamma)
        population.append(solution)
    print ('generated population is:', population)
    return population

def genetic_algorithm(params, distance_function, k, vectors, type_values, maxDomainSize):
    def evaluate_population(self, solution, solution_idx):
        params["theta1"] = solution[0]
        params["theta2"] = solution[1]  # 10
        params["betha"] = solution[2]  # 0.05
        params["gamma"] = solution[3]  # 0.01
        grades = []
        for i in range(EVALUATE_TIMES):
            model_for_population = KMeansClusterer(hyper_params=params, distance=distance_function, num_means=k,
                                                    type_of_fields=type_values)
            # activate model
            model_for_population.cluster_vectorspace(vectors)
            grades.append(model_for_population.get_wcss())
        print ('wcss:',grades,"avg",sum(grades)/len(grades))
        return (-(sum(grades)/len(grades)))
    
    
    if distance_function.__name__ != "Statistic":
        print("distance function is:",distance_function.__name__,"genetic_algorithm no matter")
        return (0, 0, 0, 0)
    
    parentMating = 2
    generationType = [int,int,float,float]
    generationSize = 4

    theta1Space = {'low':1,'high':maxDomainSize}
    theta2Space = {'low':1,'high':maxDomainSize}
    betaSpace = {'low':0,'high':1}
    gammaSpace = {'low':0,'high':1}
    generationSpace = []
    generationSpace.append(theta1Space)
    generationSpace.append(theta2Space)
    generationSpace.append(betaSpace)
    generationSpace.append(gammaSpace)

    # Generate an initial population
    population = generate_population(maxDomainSize)
    geneticAlgorithm = pygad.GA(num_generations= GENERATIONS,
                        num_parents_mating= parentMating,
                        sol_per_pop= POPULATION_SIZE,
                        num_genes= generationSize,
                        fitness_func=evaluate_population,
                        mutation_type="random",
                        mutation_probability=0.1,
                        mutation_by_replacement=True,
                        random_mutation_min_val=0,
                        initial_population=population,
                        gene_type=generationType,
                        gene_space=generationSpace)
   
    geneticAlgorithm.run()

    solution, solutionFitness, solutionIdx = geneticAlgorithm.best_solution()
    print ('solution is:',solution, 'wcss:',-solutionFitness)

    return solution
