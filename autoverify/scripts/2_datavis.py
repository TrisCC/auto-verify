from autoverify.util.instances import read_verification_result_from_json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

def main():
    # plot_data("results/cifar/results_abcrown_trained.json",
    #           "results/cifar/results_abcrown_default.json",
    #           "ABCROWN")
    
    # plot_data("results/cifar/results_mixed_trained.json",
    #           "results/cifar/results_mixed_default.json",
    #           "porfolio")
     
    # plot_data("results/cifar/results_nnenum_trained.json",
    #           "results/cifar/results_nnenum_default.json",
    #           "NNENUM")

    return 0

def plot_data(data1, data2, alg_name):
    data_1 = read_verification_result_from_json(data1)
    data_2 = read_verification_result_from_json(data2)
    
    data_1_cleaned = []
    data_2_cleaned = []
    
    if len(data_1) != len(data_2):
        data_1_cleaned = []
        data_2_cleaned = []
        seen = set()
        for i in range(len(data_1)):
            if data_1[i].network + data_1[i].property not in seen:
                seen.add(data_1[i].network + data_1[i].property)
                data_1_cleaned.append(data_1[i])
            else:
                if data_1[-1].took > data_1[i].took:
                    data_1[-1].took = data_1[i].took
        
        seen = set()     
        for i in range(len(data_2)):
            if data_2[i].network + data_2[i].property not in seen:
                seen.add(data_2[i].network + data_2[i].property)
                data_2_cleaned.append(data_2[i])
            else:
                if data_2[-1].took > data_2[i].took:
                    data_2[-1].took = data_2[i].took
                    
        data_1 = data_1_cleaned
        data_2 = data_2_cleaned
                
    # Extract data for plotting
    x = [float(item.took) for item in data_1]
    y = [float(item.took) for item in data_2]
    
    # fig, ax = plt.subplots()
    plt.axis([1, 10000, 1, 100000])
    plt.loglog()

    # Configure the plot for logarithmic scale on both axes
    # plt.figure(figsize=(8, 6))
    plt.xscale("log", base=10)
    plt.yscale("log", base=10)
    
    # Create the scatterplot with different colors for each list
    plt.scatter(x, y)
    plt.axline((0,0), (10,10), color='blue', linestyle=':')
    
    plt.xlim(0, 300)
    plt.ylim(0, 300)

    # Add labels and title
    plt.xlabel("Performance of trained model (s)")
    plt.ylabel("Performance of default model (s)")
    plt.title(f"Performance of {alg_name} on CIFAR")
    plt.legend()

    # Show the plot
    plt.grid(False)
    plt.tight_layout()
    plt.savefig(f"results/cifar/performance_{alg_name}.png")
    

if __name__ == '__main__':
    main()
    