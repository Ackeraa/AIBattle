import argparse
from game import Game
from ga import GA
from settings import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    # inherit the ancestor from the given generation
    parser.add_argument(
        "-i",
        "--inherit",
        type=int,
        help="inherit the ancestor from the given generation.",
    )

    parser.add_argument(
        "-s",
        "--show",
        action="store_true",
        help="whether to show the best individual to play game after each envolve.",
    )
    args = parser.parse_args()

    ga = GA()

    if args.inherit:
        ga.inherit_ancestor(args.inherit)
    else:
        ga.generate_ancestor()

    i = 0
    while True:
        i += 1
        ga.evolve()
        print(
            "generation: {}, best fitness: {}, average fitness: {}".format(
                ga.generation, int(ga.best_individual.fitness), int(ga.avg_fitness)
            )
        )

        # Show the best individual to play game.
        if args.show:
            genes = ga.best_individual.genes
            game = Game(genes, ga.opp_individual.genes, show=True)
            game.play()
