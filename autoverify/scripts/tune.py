from pathlib import Path

from autoverify.portfolio import Hydra, PortfolioScenario
from autoverify.util.instances import read_vnncomp_instances
from autoverify.portfolio import Hydra, PortfolioScenario
from autoverify.portfolio import ConfiguredVerifier, Portfolio, PortfolioRunner
from autoverify.util.verifiers import get_verifier_configspace

def main():
    # xs = (x * 0.3 for x in range(1, 3))
    # for x in xs:
    #     for portfolio_length in range(1, 3):
    #         print(f"Training portfolio length {portfolio_length} with alpha {x}")
    #         train_portfolio(["nnenum", "nnenum", "nnenum"], x, portfolio_length, "mnist_fc", 20)
    
    for x in [0.3, 0.6, 0.9]:
        for portfolio_length in range(1, 3):
            run_verifier(f"{portfolio_length}_{str(x)}_mnist_fc", f"results/1hour_training_mnist_fc/portfolios/PF_{portfolio_length}_{str(x)}_mnist_fc.json", "mnist_fc", 20) 
    
    # for x in [0.4, 0.8]:
    #     run_verifier(f"1_{str(x)}_CIFAR2020", f"results/1hour_training_cifar/portfolios/PF_1_{str(x)}_CIFAR2020.json", "cifar2020", 203)

    # train_portfolio(["abcrown"], 0.0, 2, "cifar2020", 5)

    return 0

def train_portfolio(verifiers_list,alpha,portfolio_length,dataset_name, dataset_cutoff):
    benchmark = read_vnncomp_instances(
        dataset_name, vnncomp_path=Path("../vnncomp/vnncomp2022/benchmarks")
    )
    benchmark = benchmark[:dataset_cutoff]
    
    pf_scenario = PortfolioScenario(
        verifiers_list,
        [
            ("nnenum", 0, 0),
        ],
        benchmark,
        portfolio_length,
        (60 * 60) * 1 / portfolio_length,
        alpha=alpha,
        output_dir=Path(f"results/1hour_training_{dataset_name}/portfolios/PF_{portfolio_length}_{str(alpha)}_{dataset_name}"),
    )

    hydra = Hydra(pf_scenario)
    pf = hydra.tune_portfolio()
    pf.to_json(Path(f"results/1hour_training_{dataset_name}/portfolios/PF_{portfolio_length}_{str(alpha)}_{dataset_name}.json"))

def run_verifier(portfolio_name, portfolio_path, dataset_name, dataset_cutoff):
    dataset = read_vnncomp_instances(
        dataset_name, vnncomp_path=Path("../vnncomp/vnncomp2022/benchmarks")
    )
    
    dataset = dataset
    
    # Run portfolio trained
    pf_trained = Portfolio.from_json(Path(portfolio_path))
    pf_runner = PortfolioRunner(pf_trained)
    pf_runner.verify_instances(
        dataset,
        out_json=Path(f"results/1hour_training_mnist_fc/runs/results_{portfolio_name}_trained.json"),
    )
    

if __name__ == '__main__':
    main()
    