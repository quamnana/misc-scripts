import subprocess
import os
from pymongo import MongoClient


def run_refactoring_miner(repo_url, pr_number, json_file):

    # Command to run RefactoringMiner
    command = [
        "./RefactoringMiner/build/distributions/RefactoringMiner-3.0.5/bin/RefactoringMiner",
        "-gp",
        repo_url,
        pr_number,
        "30",
        "-json",
        json_file,
    ]

    try:
        # Run the command
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"RefactoringMiner output for PR {pr_number}:", result.stdout)
        print(f"Refactorings for PR {pr_number} saved to", json_file)
    except subprocess.CalledProcessError as e:
        print(f"Error running RefactoringMiner for PR {pr_number}:", e.stderr)


def get_pr_data_from_mongodb():
    # MongoDB connection setup
    client = MongoClient(
        "mongodb+srv://troops:linu$008@cluster0.w4ycqka.mongodb.net/"
    )  # Adjust the connection string as needed
    db = client["first-research"]  # Replace with your database name
    pr_collection = db[
        "performance-issues-20stars"
    ]  # Replace with your collection name

    return pr_collection.find()


def main():
    # Get PR data from MongoDB
    pr_data = get_pr_data_from_mongodb()

    for i, pr in enumerate(pr_data, start=1):
        repo_name = pr["repo_name"]
        repo_url = f"{pr['repo_url']}.git"
        pr_number = pr.get("pr_number", None)

        if pr_number:
            json_file = f"ref_results/{repo_name}_pr_{pr_number}.json"
            print(
                f"================================= COLLECTING REFACTORING FROM ========================",
                repo_name,
                f"================== ({i}/{720})",
            )
            run_refactoring_miner(repo_url, str(pr_number), json_file)


if __name__ == "__main__":
    main()
