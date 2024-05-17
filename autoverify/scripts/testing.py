"""_summary_."""

from pathlib import Path

from autoverify.portfolio import ConfiguredVerifier, Portfolio, PortfolioRunner
from autoverify.util.instances import read_vnncomp_instances
from autoverify.util.verifiers import get_verifier_configspace


def main():
    """_summary_."""
    # Read benchmarks and truncate it to the first few examples
    cifar = read_vnncomp_instances(
        "cifar2020", Path("./vnncomp/vnncomp2022/benchmarks")
    )

    # Only keep every eight VerificationInstance from the cifar list
    cifar = cifar[::8]

    pf_default = Portfolio(
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

    # pf_trained = Portfolio.from_json(Path("cifar2020_nnenum_portfolio.json"))

    # pf_runner = PortfolioRunner(pf_trained)

    # pf_runner.verify_instances(
    #     cifar,
    #     out_json=Path("PF_NNENUM_cifar2020_trained_results.json"),
    # )

    # pf_trained = Portfolio.from_json(Path("cifar2020_abcrown_portfolio.json"))

    pf_runner = PortfolioRunner(pf_default)

    pf_runner.verify_instances(
        cifar,
        out_json=Path("PF_NNENUM_cifar2020_default_results.json"),
    )

    return 0


if __name__ == "__main__":
    main()
