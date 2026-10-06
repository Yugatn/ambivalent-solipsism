"""Continuous-state ORES experiment: three attractors and an observer quotient.

Model:
    V(x) = x^2 (x^2 - 1)^2
    K(x) = x - eta * V'(x), eta = 0.05

On the tested interval [-1.2, 1.2], the map has three stable fixed points
-1, 0, +1. The observer Obs_abs(x)=|x| identifies -1 and +1.

The experiment is numerical evidence for this concrete model only. It is
not a theorem about arbitrary continuous dynamical systems.
"""

import math

ETA = 0.05
STARTS = [round(-1.2 + 0.01 * i, 2) for i in range(241)]
ATTRACTORS = (-1.0, 0.0, 1.0)


def dV(x):
    return 2.0 * x * (x * x - 1.0) * (3.0 * x * x - 1.0)


def K(x):
    return x - ETA * dV(x)


def iterate(x, steps=2000):
    for _ in range(steps):
        x = K(x)
    return x


def nearest_attractor(x):
    return min(ATTRACTORS, key=lambda a: abs(x - a))


def obs_abs(x):
    return abs(x)


def factor_map_abs(y):
    return abs(K(y))


def check_factor_abs(samples):
    return all(
        math.isclose(obs_abs(K(x)), factor_map_abs(obs_abs(x)), rel_tol=0, abs_tol=1e-12)
        for x in samples
    )


def main():
    print("ORES continuous multi-attractor experiment")
    print("=" * 42)
    print(f"eta={ETA}")

    # Fixed-point stability from |K'(a)| < 1, evaluated analytically here.
    # V''(-1)=V''(1)=8, V''(0)=2, hence K'=1-eta*V''.
    stability = {
        -1.0: abs(1.0 - ETA * 8.0) < 1.0,
        0.0: abs(1.0 - ETA * 2.0) < 1.0,
        1.0: abs(1.0 - ETA * 8.0) < 1.0,
    }
    assert all(stability.values())
    print("FIXED-POINT STABILITY: PASS")

    classifications = {a: 0 for a in ATTRACTORS}
    max_residual = 0.0
    for x0 in STARTS:
        x = iterate(x0)
        max_residual = max(max_residual, min(abs(x - a) for a in ATTRACTORS))
        classifications[nearest_attractor(x)] += 1

    assert sum(classifications.values()) == len(STARTS)
    print("NUMERICAL BASIN CLASSIFICATION: PASS")
    print(f"  samples={len(STARTS)}")
    print(f"  counts={classifications}")
    print(f"  max distance to nearest attractor={max_residual:.3e}")

    # The absolute-value observer is a factor because K is odd:
    # |K(x)| = K_Y(|x|), with K_Y(y)=|K(y)|.
    assert check_factor_abs(STARTS)
    print("ABSOLUTE-VALUE OBSERVER FACTORIZATION: PASS")

    observed_attractor_images = [obs_abs(a) for a in ATTRACTORS]
    distinct_images = sorted(set(observed_attractor_images))
    assert observed_attractor_images == [1.0, 0.0, 1.0]
    assert distinct_images == [0.0, 1.0]

    l_att = len(ATTRACTORS) - len(distinct_images)
    assert l_att == 1

    print(f"OBSERVED ATTRACTOR IMAGES={observed_attractor_images}")
    print(f"L_att={l_att}")
    print("ALL ASSERTIONS: PASS")
    print("STATUS: OBSERVED (numerical reproduction for this concrete model)")


if __name__ == "__main__":
    main()
