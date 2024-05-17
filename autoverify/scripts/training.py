import sys
import csv
import time
import os
from pathlib import Path
from autoverify.portfolio import Hydra, PortfolioScenario, PortfolioRunner
from autoverify.util.instances import read_vnncomp_instances


def main():
    benchmark = read_vnncomp_instances(
        "cifar2020", vnncomp_path=Path("./vnncomp/vnncomp2022/benchmarks")
    )

    # pf_scenario = PortfolioScenario(
    #     ["nnenum", "abcrown", "ovalbab", "verinet"],
    #     [
    #         ("nnenum", 0, 0),
    #         ("verinet", 0, 1),
    #         ("abcrown", 0, 1),
    #         ("ovalbab", 0, 1),
    #     ],
    #     benchmark,
    #     4,
    #     60 * 10,
    #     alpha=0.9,
    #     output_dir=Path("PF_cifar2020"),
    # )

    # hydra = Hydra(pf_scenario)
    # pf = hydra.tune_portfolio()
    # pf.to_json(Path("cifar2020_portfolio.json"))

    pf_scenario = PortfolioScenario(
        ["abcrown"],
        [
            ("abcrown", 0, 1),
        ],
        benchmark,
        1,
        60 * 10,
        alpha=0.9,
        output_dir=Path("PF_ABCROWN_cifar2020"),
    )

    hydra = Hydra(pf_scenario)
    pf = hydra.tune_portfolio()
    pf.to_json(Path("cifar2020_abcrown_portfolio.json"))

    pf_scenario = PortfolioScenario(
        ["nnenum"],
        [
            ("nnenum", 0, 0),
        ],
        benchmark,
        1,
        60 * 10,
        alpha=0.9,
        output_dir=Path("PF_NNENUM_cifar2020"),
    )

    hydra = Hydra(pf_scenario)
    pf = hydra.tune_portfolio()
    pf.to_json(Path("cifar2020_nnenum_portfolio.json"))

    return 0


if __name__ == "__main__":
    main()
