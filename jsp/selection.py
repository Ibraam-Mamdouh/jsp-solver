"""Selection operator: tournament selection."""
from __future__ import annotations

import random
from typing import Optional

# Operation-based chromosome: each job id appears once per operation of that
# job, e.g. [0, 1, 0, 2, 1, 2]. Any permutation decodes to a valid schedule.
Chromosome = list[int]


def tournament_selection(
    population: list[Chromosome],
    fitnesses: list[int],
    k: int = 3,
    rng: Optional[random.Random] = None,
) -> Chromosome:
    """Pick k random individuals and return a copy of the best one.

    fitnesses[i] is the makespan of population[i] (lower is better).
    """
    rng = rng or random.Random()
    if len(population) != len(fitnesses):
        raise ValueError("population and fitnesses must have the same length")
    if not 1 <= k <= len(population):
        raise ValueError("k must be between 1 and the population size")

    contenders = rng.sample(range(len(population)), k)
    winner = min(contenders, key=lambda i: fitnesses[i])
    return population[winner][:]