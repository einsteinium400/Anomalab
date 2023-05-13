import random
from model.KMeanClusterer import KMeansClusterer

# Define the search space for each parameter

# Define the size of the population
population_size = 4

# Define the maximum number of generations
max_generations = 10


# # Define the fitness function
# def hello(theta1, theta2, beta, gamma):
#     # Your implementation of the hello function here
#     score=theta1+theta2+beta+gamma
#     return score


# Generate an initial population of solutions
def generate_population(beta_space, gamma_space, z):
    population = []
    for i in range(population_size):
        t = random.uniform(*[0, z])
        t2 = random.uniform(*[0, z])
        theta1 = min(t, t2)  # random.uniform(*theta1_space)
        theta2 = max(t, t2)  # random.uniform(*[theta1, z])
        beta = random.uniform(*beta_space)
        gamma = random.uniform(*gamma_space)
        solution = (theta1, theta2, beta, gamma)
        population.append(solution)
    return population


# Evaluate the fitness of each solution
def evaluate_population(params, vectors, population, distance_function, type_values, k):
    fitness_scores = []
    i = 0
    for solution in population:
        i += 1
        params["theta1"] = solution[0]
        params["theta2"] = solution[1]  # 10
        params["betha"] = solution[2]  # 0.05
        params["gamma"] = solution[3]  # 0.01


        model_for_population = KMeansClusterer(hyper_params=params, distance=distance_function, num_means=k,
                                               type_of_fields=type_values)
        # activate model
        model_for_population.cluster(vectors)
        fitness_scores.append(model_for_population.get_wcss())
    return fitness_scores


# Select parents for reproduction
def select_parents(population, fitness_scores):
    selected_parents = []
    for i in range(population_size // 2):
        parent1 = population[fitness_scores.index(min(fitness_scores))]
        fitness_scores[fitness_scores.index(min(fitness_scores))] = float("inf")
        parent2 = population[fitness_scores.index(min(fitness_scores))]
        fitness_scores[fitness_scores.index(min(fitness_scores))] = float("inf")
        selected_parents.append((parent1, parent2))
    return selected_parents


# Apply genetic operators to create a new generation
def apply_genetic_operators(selected_parents, beta_space, gamma_space, z):
    new_population = []
    for parent1, parent2 in selected_parents:
        # Crossover operator
        if random.random() < 0.5:
            child = (parent1[0], parent1[1], parent2[2], parent2[3])
        else:
            child = (parent2[0], parent2[1], parent1[2], parent1[3])

        # Mutation operator
        if random.random() < 0.1:
            theta1 = random.uniform(*[0, child[1]])
            child = (theta1, child[1], child[2], child[3])
        if random.random() < 0.1:
            theta2 = random.uniform(*[child[0], z])
            child = (child[0], theta2, child[2], child[3])
        if random.random() < 0.1:
            beta = random.uniform(*beta_space)
            child = (child[0], child[1], beta, child[3])
        if random.random() < 0.1:
            gamma = random.uniform(*gamma_space)
            child = (child[0], child[1], child[2], gamma)

        new_population.append(child)
    return new_population


def genetic_algorithm(params, distance_function, k, vectors, type_values, z):
    if distance_function.__name__ == "Hamming":
        print("genetic_algorithm no matter")

        return (0, 0, 0, 0)

    ##print("inside genetic_algoritm")    

    z = z
    # theta1_space = [0, z]
    # theta2_space = [0, 1]
    beta_space = [0, 1]
    gamma_space = [0, 1]

    # Generate an initial population
    population = generate_population(beta_space, gamma_space, z)

    # Repeat the genetic algorithm for a maximum of max_generations

    for generation in range(max_generations):
        print(generation, "###############out of", max_generations)

        # Evaluate the fitness of the current population
        fitness_scores = evaluate_population(params, vectors, population, distance_function, type_values, k)

        # Select parents for reproduction
        selected_parents = select_parents(population, fitness_scores)

        # Apply genetic operators to create a new generation
        population = apply_genetic_operators(selected_parents, beta_space, gamma_space, z)

    # Find the best solution in the final population
    best_solution = population[0]

    params["theta1"] = best_solution[0]
    params["theta2"] = best_solution[1]  # 10
    params["betha"] = best_solution[2]  # 0.05
    params["gamma"] = best_solution[3]  # 0.01

    model_for_population = KMeansClusterer(hyper_params=params, distance=distance_function, num_means=k,
                                           type_of_fields=type_values)

    # activate model
    model_for_population.cluster(vectors)

    best_fitness_score = model_for_population.get_wcss()  # hello(*best_solution)

    for solution in population[1:]:

        params["theta1"] = solution[0]
        params["theta2"] = solution[1]  # 10
        params["betha"] = solution[2]  # 0.05
        params["gamma"] = solution[3]  # 0.01

        model_for_population = KMeansClusterer(hyper_params=params, distance=distance_function,
                                               num_means=k, type_of_fields=type_values)
        # activate model
        model_for_population.cluster(vectors)

        fitness_score = model_for_population.get_wcss()  # hello(*solution)
        # if we want to find the biggest score
        if fitness_score < best_fitness_score:
            best_solution = solution
            best_fitness_score = fitness_score

    return best_solution  # , best_fitness_score
