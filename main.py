import argparse
from game import Game
from ga import GA
from settings import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-i",
        "--inherit",
        action="store_true",
        help="Whether to load genes from path ./genes/all.",
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
        ga.inherit_ancestor()
    else:
        ga.generate_ancestor()

    generation = 0
    record = 0
    while True:
        generation += 1
        ga.evolve()
        print(
            "generation: {}, record: {}, best fitness: {}, average fitness: {}".format(
                generation, record, ga.best_individual.fitness, ga.avg_fitness
            )
        )

        # Update the opponent's genes every UPDATE_GENE_STEP generation.
        if generation % UPDATE_GENE_STEP == 0:
            ga.opp_genes = ga.best_individual.genes

        # Show the best individual to play game.
        if args.show:
            genes = ga.best_individual.genes
            game = Game(genes, ga.opp_genes)
            game.play()

        # Save the best individual.
        if ga.best_individual.fitness >= record:
            record = ga.best_individual.fitness
            ga.save_best()

        # Save the population every 20 generation.
        if generation % 20 == 0:
            ga.save_all()
