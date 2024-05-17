"""_summary_."""

import gzip
import os


def unzip_gz(path):
    """Unzips all .gz files in a directory and its subdirectories.

    Args:
      path: The path to the directory containing the .gz files.
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".gz"):
                filepath = os.path.join(root, file)
                output_path = filepath[:-3]  # Remove the .gz extension

                # Open the gzipped file in binary read mode
                with gzip.open(filepath, "rb") as f_in:
                    # Open the output file in binary write mode
                    with open(output_path, "wb") as f_out:
                        # Read and write the decompressed data
                        f_out.write(f_in.read())

                print(f"Unzipped: {filepath}")

                if file.endswith("Zone.Identifier"):
                    filepath = os.path.join(root, file)
                    # Add confirmation prompt (optional)
                    # confirmation = input(f"Delete {filepath}? (y/n): ")
                    # if confirmation.lower() == "y":
                    os.remove(filepath)
                    print(f"Deleted: {filepath}")


# Specify the directory path containing the .gz files
path = "vnncomp/vnncomp2022/benchmarks"
unzip_gz(path)
