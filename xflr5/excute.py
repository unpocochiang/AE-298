import subprocess

# Path to XFLR5 executable (adjust for your system)

#mac
xflr5_path = '/Applications/xflr5.app/Contents/MacOS/xflr5'

# Run XFLR5 in batch mode with the script
subprocess.run([xflr5_path, "run_analysis.xfl"], shell=True)

# Read results into Python
with open("results.txt", "r") as file:
    results = file.readlines()

print(results)  # Process results as needed
