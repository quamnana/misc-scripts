import subprocess
from db_helpers import (
    get_all_data_from_db,
    persist_data_to_db,
    get_distict_values,
    count_data,
)


projects_collection_name = "projects-with-issues"
# collection_name = "performance-issues"


def get_non_perf_refactorings():
    projects = get_all_data_from_db(projects_collection_name)
    total_projects = count_data(projects_collection_name)

    for i, project in enumerate(projects, start=1):
        # if i in range(1473):
        #     continue

        repo_name = project["name"]
        repo_url = f"{project['html_url']}.git"
        branch = project["default_branch"]
        # destination_folder = "../projects"
        project_folder = f"projects/{repo_name}"
        json_file = f"results/{repo_name}.json"
        print(
            f"================================= COLLECTING REFACTORING FROM ========================",
            repo_name,
            f"================== ({i}/{total_projects})",
        )

        create_empty_json_file(json_file)
        git_clone(repo_url, project_folder)
        run_refactoring_miner(project_folder, branch, json_file)


def git_clone(repo_url, destination_folder):
    try:
        # Construct the git clone command
        command = ["git", "clone", repo_url, destination_folder]

        # Running the git clone command
        result = subprocess.run(command, check=True, text=True, capture_output=True)

        # Print the output
        print("Git Clone Output:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        # Handle errors in the command execution
        print(f"An error occurred: {e}")
        print("Git Clone Output:\n", e.output)
        print("Git Clone Error:\n", e.stderr)


def run_refactoring_miner(project_folder, branch, json_file):
    try:
        # Construct the command with the provided arguments
        command = [
            "./RefactoringMiner/build/distributions/RefactoringMiner-3.0.5/bin/RefactoringMiner",
            "-a",
            project_folder,
            branch,
            "-json",
            json_file,
        ]

        # Start the process and capture the output in real-time
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )

        # Read and print the output line by line in real-time
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                print(output.strip())

        # Wait for the process to finish and get the return code
        process.communicate()
        return_code = process.returncode

        # Check if the command was successful
        if return_code != 0:
            print(f"Command failed with return code {return_code}")
    except Exception as e:
        print(f"An error occurred: {e}")


def create_empty_json_file(json_file_path):
    try:
        # Open the JSON file in write mode
        with open(json_file_path, "w") as json_file:
            # Write nothing to the JSON file
            json_file.write("")

        print(f"Empty JSON file '{json_file_path}' created successfully.")
    except Exception as e:
        print(f"An error occurred while creating the JSON file: {e}")


if __name__ == "__main__":
    # run_refactoring_miner()
    get_non_perf_refactorings()
