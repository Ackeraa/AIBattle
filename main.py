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
        help="whether to show the best individual to play snake after each envolve.",
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
            "generation: {}, record: {}, best score: {}, average score: {}".format(
                generation, record, ga.best_individual.score, ga.avg_score
            )
        )

        # Update the opponent's genes every UPDATE_GENE_STEP generation.
        if generation % UPDATE_GENE_STEP == 0:
            ga.opp_genes = ga.best_individual.genes

        # Show the best individual to play snake.
        if args.show:
            genes = ga.best_individual.genes
            seed = ga.best_individual.seed
            game = Game(show=True, genes_list=[genes], seed=seed)
            game.play()

        # Save the best individual.
        if ga.best_individual.score >= record:
            record = ga.best_individual.score
            ga.save_best()

        # Save the population every 20 generation.
        if generation % 20 == 0:
            ga.save_all()
