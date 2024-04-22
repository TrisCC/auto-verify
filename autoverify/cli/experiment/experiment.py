import time
import datetime
from pathlib import Path
from result import Err, Ok
from autoverify.portfolio.hydra.hydra import Hydra
from autoverify.portfolio.portfolio import PortfolioScenario
from autoverify.verifier.verifier import CompleteVerifier
from autoverify.verifier import Nnenum, AbCrown, MnBab, OvalBab, Verinet
from autoverify.util.instances import read_vnncomp_instances

verifiers: dict[str, CompleteVerifier] = {
    "nnenum": Nnenum,
    "abcrown": AbCrown,
    "mnbab": MnBab,
    "ovalbab": OvalBab,
    "verinet": Verinet,
}


def verify_network(verifier, network, property):
    if verifier not in verifiers:
        return Err(f"No verifier found for {verifier}")

    verifier = verifiers[verifier]()

    # TODO: Check if file exists
    network_file = Path(network)
    property_file = Path(property)

    start = time.time()
    result = verifier.verify_property(network_file, property_file)
    end = time.time()

    runtime = str(datetime.timedelta(seconds=round(end - start)))

    # TODO: More elaborate results
    # TODO: Add time benchmarks
    if isinstance(result, Ok):
        outcome = result.unwrap()
        print("Verification finished")
        print("Result:", outcome.result)
        print("STDOUT:", outcome.stdout.rstrip())
        print("Took:", outcome.took)
    elif isinstance(result, Err):
        print("Error during verification:")
        print(result.unwrap_err().stdout)

    print(f"Time elapsed for verification: {runtime}")

    return


def configure_algorithm(verifier):
    if verifier not in verifiers:
        return Err(f"No verifier found for {verifier}")

    verifier = verifiers[verifier]()

    config = verifier.config_space.sample_configuration()
    print(config)

    return


def construct_portfolio(verifiers, asdas):
    instances = read_vnncomp_instances(
        "acasxu", Path("vnncomp/vnncomp2023_benchmarks/benchmarks/")
    )
    pf_scenario = PortfolioScenario(
        instances=instances,
        verifiers=["nnenum", "verinet"],
        length=4,
        resources=[],
        seconds_per_iter=10,
    )
    hydra = Hydra(pf_scenario)
    portfolio = hydra.tune_portfolio()
    portfolio.to_json("example_pf.json")

    print("WIP")
    return


def execute_portfolio(portfolio, instances):
    print("WIP")
    return
