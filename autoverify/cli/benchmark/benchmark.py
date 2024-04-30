import os
import time
import json
import shutil
import random
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
    for f in Path(path + "/onnx").iterdir():
        if f.name.endswith(".onnx"):
            res["onnx"].append(f)
    
    # Iterate through the vnnlib subfolder of the given path and add each .vnnlib file to the array in the res dict
    for f in Path(path + "/vnnlib").iterdir():
        if f.name.endswith(".vnnlib"):
            res["vnnlib"].append(f)

    return res

def run_specified_benchmark(verifier, benchmark_path):
    file_combinations = {
        "onnx": [],
        "vnnlib": []
    }
    
    files = get_benchmark_files(benchmark_path)
    
    for network_file in files["onnx"]:
        for property_file in files["vnnlib"]:
            file_combinations["onnx"].append(network_file)
            file_combinations["vnnlib"].append(property_file)
            
    run_benchmark(verifier,benchmark_path.split("/")[-1],file_combinations)
    

def run_compilation_benchmark(verifier, benchmark_path):
    
    files = get_benchmark_files(benchmark_path)
    files["onnx"].sort()
    files["vnnlib"].sort()
    
    run_benchmark(verifier,"compilation_benchmark",files)


def run_benchmark(verifier, benchmmark_name, file_combinations):
    if file_combinations["onnx"] == [] or file_combinations["vnnlib"] == []:
        raise ValueError("No files given")
    elif len(file_combinations["onnx"]) != len(file_combinations["vnnlib"]):
        raise ValueError("Number of onnx and vnnlib files must be equal")
    
    verifier_name = verifier
    verifier = verifiers[verifier]()
    
    result_summary = {
        "TOTAL_RUNTIME": 0,
        "TOTAL_RUNS": len(file_combinations["onnx"]),
        "SAT": 0,
        "UNSAT": 0,
        "TIMEOUT": 0,
        "UNKNOWN": 0,
        "ERR": 0,
        "ERR_FILES":[],
        "LONGEST_RUN_TIME": 0,
        "LONGEST_RUN_TIME_NETWORK": "",
        "LONGEST_RUN_TIME_PROPERTY": ""
    }
    
    result_detailed = {
        "run": [
        ]
    }
    
    total_combinations = len(file_combinations["onnx"])
    current_combination = 1
    
    start_total = time.time()
    for i in range(len(file_combinations["onnx"])):
        # Find file in list that matches the name of the network file but with the .vnnlib extension
        network_file = file_combinations["onnx"][i]
        property_file = file_combinations["vnnlib"][i]
        
        print(f"Verifying combination {current_combination} of {total_combinations}: {network_file.stem}...")
        
        try:
            # Start verifification and record time
            start = time.time()
            verification_result = verifier.verify_property(network_file, property_file, timeout=60)
            end = time.time()
            
            # Record longest runtime
            if end - start > result_summary["LONGEST_RUN_TIME"]:
                result_summary["LONGEST_RUN_TIME"] = end - start
                result_summary["LONGEST_RUN_TIME_NETWORK"] = str(network_file)
                result_summary["LONGEST_RUN_TIME_PROPERTY"] = str(property_file)
                
            # Record Error files
            if verification_result.value.result == "ERR":
                result_summary["ERR_FILES"].append({
                    "ONNX": network_file.stem, 
                    "VNNLIB": property_file.stem, 
                    "ERROR": verification_result.value.stdout.rstrip().splitlines()[:3] + ["..."] + verification_result.value.stdout.rstrip().splitlines()[-3:],
                    "RUNTIME": end - start})
                result_detailed["run"].append({
                    "INDEX": i,
                    "ONNX": network_file.stem, 
                    "VNNLIB": property_file.stem, 
                    "RESULT": "ERR",
                    "OUTPUT": verification_result.value.stdout.rstrip().splitlines()[:3] + ["..."] + verification_result.value.stdout.rstrip().splitlines()[-3:],
                    "RUNTIME": end - start
                })
                print(f"ERROR: {verification_result.value.stdout.rstrip().splitlines()[0]}")
            
            # Record results
            result_summary[verification_result.value.result] += 1
            result_detailed["run"].append({
                    "INDEX": i,
                    "ONNX": network_file.stem, 
                    "VNNLIB": property_file.stem, 
                    "RESULT": verification_result.value.result,
                    "OUTPUT": verification_result.value.stdout.rstrip().splitlines()[:3],
                    "RUNTIME": end - start
            })
        except Exception as e:
            # Record Error files
            result_summary["ERR_FILES"].append({
                "ONNX": network_file.stem, 
                "VNNLIB": property_file.stem, 
                "ERROR": str(e).rstrip().splitlines()[:3] + ["..."] + str(e).rstrip().splitlines()[-3:],
                "RUNTIME": end - start})
            result_detailed["run"].append({
                "INDEX": i,
                "ONNX": network_file.stem, 
                "VNNLIB": property_file.stem, 
                "RESULT": "ERR",
                "OUTPUT": verification_result.value.stdout.rstrip().splitlines()[:3] + ["..."] + verification_result.value.stdout.rstrip().splitlines()[-3:],
                "RUNTIME": end - start
            })
            print(f"ERROR: {verification_result.value.stdout.rstrip().splitlines()[0]}")
            result_summary["ERR"] += 1
        
        current_combination += 1
    end_total = time.time()
    
    result_summary["TOTAL_RUNTIME"] = end_total - start_total
    
    # Print results
    print(f"SAT: {result_summary['SAT']}")
    print(f"UNSAT: {result_summary['UNSAT']}")
    print(f"UNKNOWN: {result_summary['UNKNOWN']}")
    print(f"ERR: {result_summary['ERR']}")
    print(f"LONGEST_RUN_TIME: {result_summary['LONGEST_RUN_TIME']}")
    
    # Write res to json file
    with open(f"benchmark_results_{verifier_name}_{benchmmark_name}.json", "w") as f:
        json.dump(result_summary, f)
    with open(f"benchmark_results_detailed_{verifier_name}_{benchmmark_name}.json", "w") as f:
        json.dump(result_detailed, f)
    
    return
    

def create_compilation_benchmark(path, files_per_benchmark = 3):
    # Create folders if they don't exist
    if not os.path.exists(f"{path}/compilation_benchmark/onnx"):
        os.makedirs(f"{path}/compilation_benchmark/onnx")
    if not os.path.exists(f"{path}/compilation_benchmark/vnnlib"):
        os.makedirs(f"{path}/compilation_benchmark/vnnlib")
    
    # Iterate over all folders in the folder ./benchmarks
    for folder in os.listdir(f'{path}'):
        if folder == 'compilation_benchmark':
            continue
        
        # Put all files in a folder in a map of lists, separated by file extension
        folder_files = {"onnx": [], "vnnlib": []}
        for root, subdirs, files in os.walk(f"{path}/{folder}/"):
            for file in files:
                if file.endswith('.onnx'):
                    folder_files['onnx'] = folder_files.get('onnx', []) + [root + '/' + file]
                elif file.endswith('.vnnlib'):
                    folder_files['vnnlib'] = folder_files.get('vnnlib', []) + [root + '/' + file]
        
        if len(folder_files['onnx']) == 0 or len(folder_files['vnnlib']) == 0:
            continue
        
        for i in range(files_per_benchmark):
            random_onnx = random.choice(folder_files['onnx'])
            random_vnnlib = random.choice(folder_files['vnnlib'])
            
            # Copy the random_onnx file to the compilation_benchmark folder and rename to the folder name
            new_onnx = shutil.copy(random_onnx, f"{path}/compilation_benchmark/onnx")
            new_vnnlib = shutil.copy(random_vnnlib, f"{path}/compilation_benchmark/vnnlib")
            
            # Rename new_onnx and new_vnnlib in their folders
            os.rename(new_onnx, f"{path}/compilation_benchmark/onnx/" + folder + "_" + str(i) + ".onnx")
            os.rename(new_vnnlib, f"{path}/compilation_benchmark/vnnlib/" + folder + "_" + str(i) + ".vnnlib")
            
            if len(folder_files['onnx']) > 1:
                folder_files['onnx'].remove(random_onnx)  
            if len(folder_files['vnnlib']) > 1:
                folder_files['vnnlib'].remove(random_vnnlib)