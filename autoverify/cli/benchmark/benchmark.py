import os
from pathlib import Path
from autoverify.verifier.verifier import CompleteVerifier
from autoverify.verifier import Nnenum, AbCrown, MnBab, OvalBab, Verinet

verifiers: dict[str, CompleteVerifier] = {
    "nnenum": Nnenum,
    "abcrown": AbCrown,
    "mnbab": MnBab,
    "ovalbab": OvalBab,
    "verinet": Verinet,
}

def get_benchmark_files(path):
    res = {
        "onnx": [],
        "vnnlib": []
    }
    # Iterate through the onnx subfolder of the given path and add each .onnx file to the array in the res dict
    for f in Path(path+"/onnx").iterdir():
        if f.name.endswith(".onnx"):
            res["onnx"].append(f)
    
    # Iterate through the vnnlib subfolder of the given path and add each .vnnlib file to the array in the res dict
    for f in Path(path+"/vnnlib").iterdir():
        if f.name.endswith(".vnnlib"):
            res["vnnlib"].append(f)

    return res

def run_benchmark(verifier, benchmark_path):
    files = get_benchmark_files(benchmark_path)
    
    verifier = verifiers[verifier]()
    
    res = {
        "SAT": 0,
        "UNSAT": 0,
        "UNKNOWN": 0
        "LONGEST_RUN_TIME": 0,
        "LONGEST_RUN_TIME_NETWORK": "",
        "LONGEST_RUN_TIME_PROPERTY": ""
    }

    for network_file in files["onnx"]:
        for property_file in files["vnnlib"]:
            start = time.time()
            verification_result = verifier.verify_property(network_file, property_file)
            end = time.time()
            if end - start > res["LONGEST_RUN_TIME"]:
                res["LONGEST_RUN_TIME"] = end - start
                res["LONGEST_RUN_TIME_NETWORK"] = network_file
                res["LONGEST_RUN_TIME_PROPERTY"] = property_file
            res[verification_result.value.result] += 1
    
    print(f"SAT: {res['SAT']}")
    print(f"UNSAT: {res['UNSAT']}")
    print(f"UNKNOWN: {res['UNKNOWN']}")
    print(f"LONGEST_RUN_TIME: {res['LONGEST_RUN_TIME']}")
    
    # Write res to json file
    with open("benchmark_results.json", "w") as f:
        json.dump(res, f)
    
    return
