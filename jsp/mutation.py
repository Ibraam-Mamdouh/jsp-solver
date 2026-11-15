"""Mutation operator: swap mutation."""
from __future__ import annotations

import random
from typing import Optional

# Operation-based chromosome: each job id appears once per operation of that
# job, e.g. [0, 1, 0, 2, 1, 2]. Any permutation decodes to a valid schedule.
Chromosome = list[int]


def swap_mutation(
    chromosome: Chromosome,
    mutation_rate: float = 0.1,
    rng: Optional[random.Random] = None,
) -> Chromosome:
    """With probability `mutation_rate`, swap two genes of different jobs.

    Returns a new chromosome; the input is never modified. Swapping keeps
    the count of every job id, so the result is still a valid chromosome.
    """
    rng = rng or random.Random()
    if not 0.0 <= mutation_rate <= 1.0:
        raise ValueError("mutation_rate must be between 0 and 1")

    child = chromosome[:]
    if len(child) < 2 or rng.random() >= mutation_rate:
        return child

    i = rng.randrange(len(child))
    candidates = [j for j in range(len(child)) if child[j] != child[i]]
    if not candidates:          # all genes are the same job: nothing to swap
        return child
    j = rng.choice(candidates)
    child[i], child[j] = child[j], child[i]
    return child