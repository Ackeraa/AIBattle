import random
import numpy as np
import copy
from game import Game
from settings import *
import os


class Individual:
    """Individual in population of Genetic Algorithm.
    Attributes:
        genes: A list which can transform to weight of Neural Network.
        ticks: The time of the game.
        player_hp: HP of player.
        opp_hp: HP of opponent.
        fitnees: Fitness of Individual.
    """

    def __init__(self, genes):
        self.genes = genes
        self.ticks = 1
        self.player_hp = 0
        self.opp_hp = 0
        self.fitness = 0

    def _h(self, x, y, z):
        """
        x: player's hp [0..PLAYER1_HP]
        y: opp's hp [0..PLAYER2_HP]
        z: ticks [0..MAX_TICKS]
        """
        x /= PLAYER1_HP
        y /= PLAYER2_HP
        z /= MAX_TICKS

        wx = 0.2
        wy = -0.7
        wz = -0.1

        return (wx * x + wy * y + wz * z + 0.8) * 10000

    def get_fitness(self, opp_genes):
        """Get the fitness of Individual."""
        game = Game(self.genes, opp_genes)
        self.player_hp, self.opp_hp, self.ticks = game.play()
        self.fitness = self._h(self.player_hp, self.opp_hp, self.ticks)


class GA:
    """Genetic Algorithm.
    Attributes:
        p_size: Size of the parent generation.
        c_size: Size of the child generation.
        genes_len: Length of the genes.
        mutate_rate: Probability of the mutation.
        population: A list of individuals.
        best_individual: Individual with best fitness.
        avg_fitness: Average ticks of the population.
    """

    def __init__(
        self, p_size=P_SIZE, c_size=C_SIZE, genes_len=GENES_LEN, mutate_rate=MUTATE_RATE
    ):
        self.generation = 0
        self.p_size = p_size
        self.c_size = c_size
        self.genes_len = genes_len
        self.mutate_rate = mutate_rate
        self.population = []
        self.best_individual = None  # in current generation
        self.avg_fitness = 0
        self.opp_individual = Individual(np.random.uniform(-1, 1, genes_len))
        self.update_step = INIT_UPDATE_GAP

    def generate_ancestor(self):
        for _ in range(self.p_size):
            genes = np.random.uniform(-1, 1, self.genes_len)
            self.population.append(Individual(genes))

    def inherit_ancestor(self, generation):
        """Load genes from './genes/{generation}'."""
        for filename in os.listdir(os.path.join("genes", str(generation))):
            if not filename.startswith("opp") and not filename.startswith("best"):
                genes_pth = os.path.join("genes", str(generation), filename)
                with open(genes_pth, "rb") as f:
                    genes = np.load(f)
                    self.population.append(Individual(genes))

    def crossover(self, c1_genes, c2_genes):
        """Single point crossover."""
        point = np.random.randint(0, self.genes_len)
        c1_genes[: point + 1], c2_genes[: point + 1] = (
            c2_genes[: point + 1],
            c1_genes[: point + 1],
        )

    def mutate(self, c_genes):
        """Gaussian mutation with scale of 0.2."""
        mutation_array = np.random.random(c_genes.shape) < self.mutate_rate
        mutation = np.random.normal(size=c_genes.shape)
        mutation[mutation_array] *= 0.2
        c_genes[mutation_array] += mutation[mutation_array]

    def elitism_selection(self, size):
        """Select the top #size individuals to be parents."""
        population = sorted(
            self.population, key=lambda individual: individual.fitness, reverse=True
        )
        return population[:size]

    def roulette_wheel_selection(self, size):
        selection = []
        wheel = sum(individual.fitness for individual in self.population)
        for _ in range(size):
            pick = np.random.uniform(0, wheel)
            current = 0
            for individual in self.population:
                current += individual.fitness
                if current >= pick:
                    selection.append(individual)
                    break

        return selection

    def evolve(self):
        """The main procss of Genetic Algorithm."""
        sum_fitness = 0
        for individual in self.population:
            individual.get_fitness(self.opp_individual.genes)
            sum_fitness += individual.fitness
        self.avg_fitness = sum_fitness / len(self.population)

        # Select parents to generate children.
        self.population = self.elitism_selection(self.p_size)
        self.best_individual = self.population[0]
        random.shuffle(self.population)

        # Generate children.
        children = []
        while len(children) < self.c_size:
            p1, p2 = self.roulette_wheel_selection(2)
            c1_genes, c2_genes = p1.genes.copy(), p2.genes.copy()
            self.crossover(c1_genes, c2_genes)
            self.mutate(c1_genes)
            self.mutate(c2_genes)
            c1, c2 = Individual(c1_genes), Individual(c2_genes)
            children.extend([c1, c2])

        random.shuffle(children)
        self.population.extend(children)

        self.generation += 1

        if self.generation % self.update_step == 0:
            self.save()
            self.opp_individual = copy.deepcopy(self.best_individual)
            self.update_step += int(self.update_step * UPDATE_RATE)

    def save(self):
        """Save the best individual, the opponent's genes and the population."""
        file_path = os.path.join("genes", str(self.generation))
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        else:
            for file in os.listdir(file_path):
                os.remove(os.path.join(file_path, file))

        self._save_best()
        self._save_opp()
        self._save_all()

    def _save_best(self):
        """Save the best individual so far."""
        fitness = int(self.best_individual.fitness)
        genes_pth = os.path.join("genes", str(self.generation), f"best_{fitness}")
        with open(genes_pth, "wb") as f:
            np.save(f, self.best_individual.genes)

    def _save_opp(self):
        """Save the opponent's genes."""
        self.opp_individual.get_fitness(self.best_individual.genes)
        fitness = int(self.opp_individual.fitness)
        genes_pth = os.path.join("genes", str(self.generation), f"opp_{fitness}")
        with open(genes_pth, "wb") as f:
            np.save(f, self.opp_individual.genes)

    def _save_all(self):
        """Save the population."""
        for individual in self.population:
            individual.get_fitness(self.opp_individual.genes)
        population = self.elitism_selection(self.p_size)
        for i in range(len(population)):
            fitness = int(population[i].fitness)
            genes_pth = os.path.join("genes", str(self.generation), f"{i}_{fitness}")
            with open(genes_pth, "wb") as f:
                np.save(f, population[i].genes)
