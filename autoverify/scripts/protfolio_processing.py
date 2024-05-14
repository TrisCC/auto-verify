import os
import pandas as pd
import numpy as np
import sys
import json
from pathlib import Path
from autoverify.util.instances import read_vnncomp_instances, read_verification_result_from_json


def main():
    
    all_results = [
        read_verification_result_from_json("PF_ABCROWN_cifar2020_default_results.json"),
        read_verification_result_from_json("PF_ABCROWN_cifar2020_trained_results.json"),
        read_verification_result_from_json("PF_NNENUM_cifar2020_default_results.json"),
        read_verification_result_from_json("PF_NNENUM_cifar2020_trained_results.json"),
        read_verification_result_from_json("PF_ABCROWN_NNENUM_cifar2020_default_results.json"),
        read_verification_result_from_json("PF_ABCROWN_NNENUM_cifar2020_trained_results.json"),
        ]
    
    output = []
    
    for index, result in enumerate(all_results[0]):
        output.append({
            "network": Path(result.network).stem,
            "property": Path(result.property).stem,
            "ABCROWN_DEFAULT": all_results[0][index].success,
            "ABCROWN_TRAINED": all_results[1][index].success,
            "NNENUM_DEFAULT": all_results[2][index].success,
            "NNENUM_TRAINED": all_results[3][index].success,
            "ABCROWN_NNENUM_DEFAULT": all_results[4][index].success,
            "ABCROWN_NNENUM_TRAINED": all_results[5][index].success,
        })

    with open(f"cifar2020_processed.json", "w") as f:
        json.dump(output, f)
    
    return 0

if __name__ == '__main__':
    main()
    