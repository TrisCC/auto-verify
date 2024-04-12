import time
import datetime
from pathlib import Path
from result import Err, Ok
from autoverify.verifier import Nnenum


def verify_network(verifier, network, property):
    # TODO: Parse verifier type
    verifier = Nnenum()

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
        outcome = result.unwrap().result
        print("Verification finished, result:", outcome)
    elif isinstance(result, Err):
        print("Error during verification:")
        print(result.unwrap_err().stdout)

    print(f"Time elapsed for verification: {runtime}")

    return


if __name__ == "__main__":
    verifier = Nnenum()

    network = Path("tests/fake_vnncomp/trivial/onnx/test_nano.onnx")
    prop = Path("tests/fake_vnncomp/trivial/vnnlib/test_nano.vnnlib")

    result = verifier.verify_property(network, prop)

    if isinstance(result, Ok):
        outcome = result.unwrap().result
        print("Verification finished, result:", outcome)
    elif isinstance(result, Err):
        print("Error during verification:")
        print(result.unwrap_err().stdout)
