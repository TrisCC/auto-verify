from pathlib import Path

from autoverify.portfolio import Hydra, PortfolioScenario
from autoverify.util.instances import read_vnncomp_instances
from autoverify.portfolio import Hydra, PortfolioScenario
from autoverify.portfolio import ConfiguredVerifier, Portfolio, PortfolioRunner
from autoverify.util.verifiers import get_verifier_configspace

def main():
    train_portfolio()
    train_nnenum()
    train_abcrown()
    run_cifar()

    return 0

def train_portfolio():
    benchmark = read_vnncomp_instances(
        "cifar2020", vnncomp_path=Path("./vnncomp/vnncomp2022/benchmarks")
    )
    benchmark = benchmark[::4]
    
    pf_scenario = PortfolioScenario(
        ["abcrown", "nnenum"],
        [
            ("abcrown", 0, 1),
            ("nnenum", 0, 0),
        ],
        benchmark,
        2,
        60 * 60,
        alpha=0.7,
        output_dir=Path("results/4hour_training_cifar/portfolios/PF_2_MIX_CIFAR2020"),
    )

    hydra = Hydra(pf_scenario)
    pf = hydra.tune_portfolio()
    pf.to_json(Path("results/4hour_training_cifar/portfolios/PF_2_MIX_CIFAR2020.json"))
    
def train_nnenum():
    benchmark = read_vnncomp_instances(
        "cifar2020", vnncomp_path=Path("./vnncomp/vnncomp2022/benchmarks")
    )
    benchmark = benchmark[::4]
    
    pf_scenario = PortfolioScenario(
        ["nnenum"],
        [
            ("nnenum", 0, 0),
        ],
        benchmark,
        1,
        60 * 60,
        alpha=0.7,
        output_dir=Path("results/4hour_training_cifar/portfolios/PF_1_NNENUM_CIFAR2020"),
    )

    hydra = Hydra(pf_scenario)
    pf = hydra.tune_portfolio()
    pf.to_json(Path("results/4hour_training_cifar/portfolios/PF_1_NNENUM_CIFAR2020.json"))
    
def train_abcrown():
    benchmark = read_vnncomp_instances(
        "cifar2020", vnncomp_path=Path("./vnncomp/vnncomp2022/benchmarks")
    )
    benchmark = benchmark[::4]
    
    pf_scenario = PortfolioScenario(
        ["abcrown"],
        [
            ("abcrown", 1, 0),
        ],
        benchmark,
        1,
        60 * 60,
        alpha=0.7,
        output_dir=Path("results/4hour_training_cifar/portfolios/PF_1_ABCROWN_CIFAR2020"),
    )

    hydra = Hydra(pf_scenario)
    pf = hydra.tune_portfolio()
    pf.to_json(Path("results/4hour_training_cifar/portfolios/PF_1_ABCROWN_CIFAR2020.json"))

def run_cifar():
    cifar = read_vnncomp_instances(
        "cifar2020", vnncomp_path=Path("./vnncomp/vnncomp2022/benchmarks")
    )
    
    # Run ABCROWN trained
    pf_trained = Portfolio.from_json(Path("results/4hour_training_cifar/portfolios/PF_1_ABCROWN_CIFAR2020.json"))
    pf_runner = PortfolioRunner(pf_trained)
    pf_runner.verify_instances(
        cifar,
        out_json=Path("results/4hour_training_cifar/cifar/results_abcrown_trained.json"),
    )
    
    # Run NNENUM trained
    pf_trained = Portfolio.from_json(Path("results/4hour_training_cifar/portfolios/PF_1_NNENUM_CIFAR2020.json"))
    pf_runner = PortfolioRunner(pf_trained)
    pf_runner.verify_instances(
        cifar,
        out_json=Path("results/4hour_training_cifar/cifar/results_nnenum_trained.json"),
    )
    
    # Run portfolio trained
    pf_trained = Portfolio.from_json(Path("results/4hour_training_cifar/portfolios/PF_2_MIX_CIFAR2020.json"))
    pf_runner = PortfolioRunner(pf_trained)
    pf_runner.verify_instances(
        cifar,
        out_json=Path("results/4hour_training_cifar/cifar/results_nnenum_trained.json"),
    )
    

if __name__ == '__main__':
    main()
    