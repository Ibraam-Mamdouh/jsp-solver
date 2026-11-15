"""Crossover operator: Job-based Order Crossover (JOX)."""
from __future__ import annotations

import random
from typing import Optional

# Operation-based chromosome: each job id appears once per operation of that
# job, e.g. [0, 1, 0, 2, 1, 2]. Any permutation decodes to a valid schedule.
Chromosome = list[int]


def _jox_child(a: Chromosome, b: Chromosome, keep: set[int]) -> Chromosome:
    """Keep genes of the `keep` jobs from a at their positions;
    fill the remaining positions from b in b's order."""
    fill = (g for g in b if g not in keep)
    return [g if g in keep else next(fill) for g in a]


def jox_crossover(
    parent1: Chromosome,
    parent2: Chromosome,
    rng: Optional[random.Random] = None,
) -> tuple[Chromosome, Chromosome]:
    """Job-based Order Crossover (JOX). Returns two children."""
    rng = rng or random.Random()
    if len(parent1) != len(parent2):
        raise ValueError("parents must have the same length")

    jobs = sorted(set(parent1))
    if len(jobs) < 2:
        return parent1[:], parent2[:]

    keep = set(rng.sample(jobs, rng.randint(1, len(jobs) - 1)))
    return _jox_child(parent1, parent2, keep), _jox_child(parent2, parent1, keep)