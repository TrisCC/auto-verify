import sys
import csv
import time
import os
import json
from pathlib import Path
from autoverify.portfolio import (
    Hydra,
    PortfolioScenario,
    PortfolioRunner,
    Portfolio,
)
from autoverify.util.instances import read_vnncomp_instances
from autoverify.util.verifiers import get_verifier_configspace
from autoverify.portfolio import ConfiguredVerifier


def main():
    # Read benchmarks and truncate it to the first few examples
    cifar = read_vnncomp_instances(
        "cifar2020", Path("./vnncomp/vnncomp2022/benchmarks")
    )

    # Read results json in ./results/
    results = json.load(open(Path("./results/cifar2020_notable_results.json")))

    # Create filtered list of the cifar list where the remaining list has the same network and property name as an entry in the results list
    filtered_cifar = []
    for instance in cifar:
        for result in results:
            if (
                instance.network.stem == result["network"]
                and instance.property.stem == result["property"]
            ):
                filtered_cifar.append(instance)
                break

    pf = Portfolio.from_json(Path("./results/cifar2020_portfolio.json"))

    pf = Portfolio(
        ConfiguredVerifier(
            "nnenum",
            get_verifier_configspace("nnenum").get_default_configuration(),
            (8, 0),
        ),
        # ConfiguredVerifier(
        #     "abcrown",
        #     get_verifier_configspace("abcrown").get_default_configuration(),
        #     (2, 1),
        # ),
    )

    pf_runner = PortfolioRunner(pf)

    pf_runner.verify_instances(
        filtered_cifar,
        out_json=Path("analysis.json"),
    )

    return 0


if __name__ == "__main__":
    main()
