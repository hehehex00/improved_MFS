import os
from pathlib import Path

# To create a freeze.txt file run this from the src directory:
#   pip freeze -r requirements.txt > freeze.txt

# Find all packages in freeze file and add to dictionary
packages: dict = {}
with Path("freeze.txt").open() as packages_file:
    for line in packages_file:
        if "==" in line:
            package: str = line.split("==")[0]
            version: str = line.split("==")[1]
            packages.update({package: version})

# Loop through tools directory
toolbox_folder: str = "./data_toolbox"
for tool_folder in os.listdir(toolbox_folder):
    tool_req_path: str = f"{toolbox_folder}/{tool_folder}/requirements.txt"

    # Check if requirements.txt exists
    if Path(tool_req_path).is_file():
        print(f"\nUpdating {tool_folder} requirements")

        # Open file as readonly, capturing in a list for indexing
        with Path(tool_req_path).open() as tool_packages:
            data: list = tool_packages.readlines()

            # Iterate through lines in file
            for i in range(len(data)):
                line = data[i]

                # If package in file but not assigned version, assign it
                for package, version in packages.items():
                    if package == line.strip() and "==" not in line:
                        print(f"{line.strip()} : {package} - {version.strip()}")
                        data[i] = f"{package}=={version}"
                        break

        # Write back to file
        with Path(tool_req_path).open("w") as tool_packages:
            tool_packages.writelines(data)

# Do the same as above to root requirements.txt
root_req_path: str = "./requirements.txt"

# Check if requirements.txt exists
if Path(root_req_path).is_file():
    print("\nUpdating root requirements")
    # Open file as readonly, capturing in a list for indexing
    with Path(root_req_path).open() as tool_packages:
        data: list = tool_packages.readlines()
        # Iterate through lines in file
        for i in range(len(data)):
            line = data[i]
            # If package in file but not assigned version, assign it
            for package, version in packages.items():
                if package == line.strip() and "==" not in line:
                    print(f"{line.strip()} : {package} - {version.strip()}")
                    data[i] = f"{package}=={version}"
                    break
    # Write back to file
    with Path(root_req_path).open("w") as tool_packages:
        tool_packages.writelines(data)
