from init import *
from optimization import *
from json import dumps
from limit import achieved

num = 10  # number of Chaotic maps

if __name__ == '__main__':
    print("Bacterial Foraging Optimization Algorithm")
    print("Dimension: ", dimension)
    # For tracking global minima. ;)
    results = {}
    for i in range(num):
        best = INF                 # the best solution found during the search
        fe_count = 0               # number of objective function evaluations
        # search space [-100, 100]^dimension
        c_tumble, c_space, c_prob, space = initialize_space(
            space, -100.0, 100.0)
        # random initialization within the search space
        population, c_space, fe_count, best = initialize_population(
            i+1, population, c_space, fe_count, best)
        # minimization of objective function
        best = optimization(
            i+1, population, c_space, fe_count, best, c_prob, c_tumble)
        if best == 0.0:
            results[str(i+1)] = 1.0
        else:
            results[str(i+1)] = best
        results['c_space'], results['c_prob'], results[
            'c_tumble'] = c_space, c_prob, c_tumble

    for x in results:
        if x in achieved and results[x] > achieved[x]:
            results[x] = achieved[x]
    with open('data.py', 'a') as f:
            f.write(dumps(results) + '\n')
    if results != achieved:
        with open('limit.py', 'w') as f:
            f.write("achieved = " + dumps(results))
            print("Updated!")