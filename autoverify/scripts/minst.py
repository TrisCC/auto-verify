"""_summary_."""

import json
import time
from pathlib import Path

from autoverify.util.instances import read_vnncomp_instances
from autoverify.verifier import AbCrown


def main():
    """_summary_."""
    minst_instances = read_vnncomp_instances(
        "cifar2020", Path("./vnncomp/vnncomp2022/benchmarks")
    )
    result_summary = {
        "TOTAL_RUNTIME": 0,
        "TOTAL_RUNS": len(minst_instances),
        "SAT": 0,
        "UNSAT": 0,
        "TIMEOUT": 0,
        "UNKNOWN": 0,
        "ERR": 0,
        "ERR_FILES": [],
        "LONGEST_RUN_TIME": 0,
        "LONGEST_RUN_TIME_NETWORK": "",
        "LONGEST_RUN_TIME_PROPERTY": "",
    }

    ERR_FILES = []

    try:
        abcrown_verifier = AbCrown()

        config = abcrown_verifier.config_space.sample_configuration()
        print(config)

        start = time.time()
        for index, instance in enumerate(minst_instances):
            if instance.network.stem == "mnist-net_256x4":
                result_summary["TOTAL_RUNS"] = (
                    int(str(result_summary["TOTAL_RUNS"])) + 1
                )
                break

            print(
                f"Verifying instance {index+1} of {len(minst_instances)}:"
                + f"{instance.network.stem} {instance.property.stem}"
            )
            verification_result = abcrown_verifier.verify_instance(instance)

            result_summary[verification_result.value.result] = (
                int(str(result_summary[verification_result.value.result])) + 1
            )

            if verification_result.value.result == "ERR":
                ERR_FILES.append(
                    {
                        "ONNX": instance.network.stem,
                        "VNNLIB": instance.property.stem,
                        "ERROR": verification_result.value.stdout.splitlines()[
                            :3
                        ]
                        + ["..."]
                        + verification_result.value.stdout.splitlines()[-3:],
                        "RUNTIME": verification_result.value.took,
                    }
                )
                print(
                    "ERROR: "
                    + verification_result.value.stdout.rstrip().splitlines()[0]
                )
        result_summary["ERR_FILES"] = ERR_FILES
        total_time = time.time() - start
        result_summary["TOTAL_RUNTIME"] = total_time
        print(f"TOTAL_RUNTIME: {total_time}")

    except KeyboardInterrupt:
        print("Interrupted")

    with open("benchmark_results_abcrown_cifar_conf.json", "w") as f:
        json.dump(result_summary, f)


if __name__ == "__main__":
    main()
