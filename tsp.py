import math
import random
from astar import AStar


class ShortestPath:
    def __init__(self, start, tasks, costs):
        self.tasks = tasks
        self.start = start
        self.costs = costs
        super().__init__()

    def path_cost(self, paths):
        i = 0
        costs = 0
        current_position = self.start
        for path in paths:
            cost = AStar(
                current_position[0],  # x
                current_position[1],  # y
                current_position[2],  # direction
                path['coordinates'][0],
                path['coordinates'][1],
                self.costs
            ).process(show_cost=True)
            i += 1
            costs += cost[0]
            current_position = (
                cost[1][-1][0],
                cost[1][-1][1],
                cost[1][-1][2],
            )
        return costs

    def crossover_cost(self, crossover):
        i = 0
        costs = 0
        current_position = self.start
        for path in crossover:
            cost = AStar(
                current_position[0],  # x
                current_position[1],  # y
                current_position[2],  # direction
                path['coordinates'][0],
                path['coordinates'][1],
                self.costs
            ).process(show_cost=True)
            i += 1
            costs += cost[0]
            current_position = (
                cost[1][-1][0],
                cost[1][-1][1],
                cost[1][-1][2],
            )
        return costs

    def mutate(self, path):
        key1 = random.randint(0, len(path) - 1)
        key2 = random.randint(0, len(path) - 1)
        while key2 == key1:
            key2 = random.randint(0, len(path) - 1)

        temp = path[key1]
        path[key1] = path[key2]
        path[key2] = temp

        return path

    def sort(self, population):
        return sorted(population, key=lambda x: x[0])

    def get_shortest_path(self):
        tasks = self.tasks.copy()
        iteration_number = int(math.ceil(len(tasks) / 2))
        crossover_number = int(math.ceil(len(tasks) / 3))
        population = []
        for l in range(len(tasks)):
            temp_tasks = random.sample(tasks, len(tasks))
            population.append(
                (self.path_cost(temp_tasks), temp_tasks)
            )
        population_length = len(population)

        for _ in range(iteration_number):
            used_keys = []
            for _ in range(crossover_number):
                key1 = random.randint(0, len(population) - 1)
                while key1 in used_keys:
                    key1 = random.randint(0, len(population) - 1)
                used_keys.append(key1)
                key2 = random.randint(0, len(population) - 1)
                while key2 in used_keys:
                    key2 = random.randint(0, len(population) - 1)
                used_keys.append(key2)

                cross1 = (population[key1][0], population[key1][1])
                cross2 = (population[key2][0], population[key2][1])

                crossover = []
                for i in range(iteration_number):
                    crossover.append(cross1[1][i])

                for elem in cross2[1]:
                    if elem not in crossover:
                        crossover.append(elem)

                population.append(
                    (self.path_cost(crossover), crossover)
                )
            mutation_key = random.randint(0, len(population) - 1)
            mutation_result = self.mutate(population[mutation_key][1])
            population[mutation_key] = (
                self.path_cost(mutation_result),
                mutation_result
            )
            population = self.sort(population)[:population_length]

        return population[0][1]
