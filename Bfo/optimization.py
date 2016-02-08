"""Runs the algorithm for the three main steps."""
from init import *


def optimization():
    for l in range(N_ed):
        for k in range(N_re):
            for j in range(N_ch):
                chemotaxis()
                printf("best = %s, fe_count = %s", best, fe_count)
            reproduction()
        elimination_dispersal()
    print(
        "best found value: %s, number of function evaluations: %s", best,
        fe_count)


def chemotaxis():
    Jlast = 0.0
    new_cell = Cell()
    for i in range(S):
        interaction(population[i])
        Jlast = population[i].fitness
        tumble_step(new_cell, population[i])  # tumble i bactu nd save new cell
        objective_function(new_cell)
        interaction(new_cell)
        for j in range(dimension):
            population[i].vect[j] = new_cell.vect[j]
        population[i].cost = new_cell.cost
        population[i].fitness = new_cell.fitness
        population[i].health += population[i].fitness

        for m in range(N_sl):
            if new_cell.fitness < Jlast:
                Jlast = new_cell.fitness
                swim_step(new_cell, population[i])

                objective_function(new_cell)
                interaction(new_cell)

                # copy
                for j in range(dimension):
                    population[i].vect[j] = new_cell.vect[j]
                population[i].cost = new_cell.cost
                population[i].fitness = new_cell.fitness
                population[i].health += population[i].fitness

            else:
                break


def gethealth(bact):
    return bact.health


def reproduction():
    # sort the population in order of increasing health value
    population = sorted(population, key=gethealth, reverse=True)

    # Sr healthiest bacteria split into two bacteria, which are placed at the
    # same location
    i, j = S-Sr, 0
    while j < Sr:
        population[i] = population[j]
        i, j = i+1, j+1

    for i in range(Sr, S):
        population[i].health = 0.0


def elimination_dispersal():
    """
    # Elimination and dispersal event.
    """
    for i in range(S):
        # simply disperse bacterium to a random location on the search space
        if randint(0.0, 1.0) < p_ed:
            for j in range(dimension):
                population[i].vect[j] = randint(space[j][0], space[j][1])
            objective_function(population[i])


def objective_function(x):

    rez = 0.0
    fe_count += 1

    # Sphere Function
    for i in range(dimension):
        rez += pow(x.vect[i], 2.0)

    x.cost = rez

    if x.cost < best:
        best = x.cost