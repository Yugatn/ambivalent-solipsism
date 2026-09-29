"""Reproducible finite-state experiment for ORES observer quotients.

The script implements the mathematical model in
DEVELOPMENT/ORES_MINIMAL_MULTI_ATTRACTOR_OBSERVERS.md and checks:
- attractor/basin classification;
- observer fibres;
- observed attractor classes;
- factor-dynamics compatibility;
- the non-factor counterexample Obs_4;
- the discrete distinguishability loss L_att.

No stochastic components are used.
"""

from collections import defaultdict

STATES = ("a", "b", "c", "u", "v")

K = {
    "a": "a",
    "b": "b",
    "c": "c",
    "u": "a",
    "v": "b",
}

ATTRACTORS = (frozenset(("a",)), frozenset(("b",)), frozenset(("c",)))


def iterate(x, n=10):
    for _ in range(n):
        x = K[x]
    return x


def basin(attractor):
    return frozenset(x for x in STATES if iterate(x) in attractor)


def fibres(observer):
    out = defaultdict(set)
    for x, y in observer.items():
        out[y].add(x)
    return {y: frozenset(xs) for y, xs in out.items()}


def observed_attractor_classes(observer):
    return {
        i: frozenset(observer[next(iter(A))] for _ in [0])
        for i, A in enumerate(ATTRACTORS, start=1)
    }


def factor_map(observer):
    """Return the unique induced map if Obs o K = K_Y o Obs; otherwise None."""
    induced = {}
    for x in STATES:
        y = observer[x]
        y_next = observer[K[x]]
        if y in induced and induced[y] != y_next:
            return None
        induced[y] = y_next
    return induced


def check_factor(observer):
    ky = factor_map(observer)
    if ky is None:
        return False, None
    return all(observer[K[x]] == ky[observer[x]] for x in STATES), ky


def attractor_class_count(observer):
    return len(set(observer[next(iter(A))] for A in ATTRACTORS))


def l_att(observer):
    return len(ATTRACTORS) - attractor_class_count(observer)


OBSERVERS = {
    "Obs_1_identity": {x: x for x in STATES},
    "Obs_2_merge_A1_A2": {
        "a": "alpha", "b": "alpha", "c": "beta",
        "u": "alpha", "v": "alpha",
    },
    "Obs_3_basin": {
        "a": "B1", "u": "B1",
        "b": "B2", "v": "B2",
        "c": "B3",
    },
    "Obs_4_nonfactor": {
        "a": "delta", "b": "delta", "c": "epsilon",
        "u": "epsilon", "v": "delta",
    },
}


def main():
    print("ORES finite observer experiment")
    print("=" * 32)

    expected_basins = (
        frozenset(("a", "u")),
        frozenset(("b", "v")),
        frozenset(("c",)),
    )
    actual_basins = tuple(basin(A) for A in ATTRACTORS)
    assert actual_basins == expected_basins
    print("ATTRACTORS/BASINS: PASS")

    for name, obs in OBSERVERS.items():
        fs = fibres(obs)
        factor_ok, ky = check_factor(obs)
        print(f"\\n{name}")
        print(f"  fibres = {dict(fs)}")
        print(f"  attractor_classes = {attractor_class_count(obs)}")
        print(f"  L_att = {l_att(obs)}")
        print(f"  factor_dynamics = {factor_ok}")
        if ky is not None:
            print(f"  K_Y = {ky}")

    assert check_factor(OBSERVERS["Obs_1_identity"])[0]
    assert check_factor(OBSERVERS["Obs_2_merge_A1_A2"])[0]
    assert check_factor(OBSERVERS["Obs_3_basin"])[0]
    assert not check_factor(OBSERVERS["Obs_4_nonfactor"])[0]

    assert l_att(OBSERVERS["Obs_1_identity"]) == 0
    assert l_att(OBSERVERS["Obs_2_merge_A1_A2"]) == 1
    assert l_att(OBSERVERS["Obs_3_basin"]) == 0

    print("\\nALL ASSERTIONS: PASS")
    print("STATUS: OBSERVED (deterministic computational reproduction)")


if __name__ == "__main__":
    main()
