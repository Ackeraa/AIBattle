from game import Game


class Individual:
    """Individual in population of Genetic Algorithm.
    Attributes:
        genes: A list which can transform to weight of Neural Network.
        score: Score of the snake played by its Neural Network.
        steps: Steps of the snake played by its Neural Network.
        fitnees: Fitness of Individual.
        seed: The random seed of the game, saved for reproduction.
    """

    def __init__(self, genes):
        self.genes = genes
        self.score = 0
        self.steps = 0
        self.fitness = 0
        self.seed = None

    def get_fitness(self):
        """Get the fitness of Individual."""
        game = Game([self.genes])
        self.score, self.steps, self.seed = game.play()
        self.fitness = (self.score + 1 / self.steps) * 100000
