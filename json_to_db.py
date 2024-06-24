import os
import json
import re
from pymongo import MongoClient

# MongoDB configuration
MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "first-research"
COLLECTION_NAME = "projects-refactorings"
JSON_DIRECTORY = "/Users/nanaquam/Library/CloudStorage/GoogleDrive-quamgyambrah@gmail.com/My Drive/refactoring_miner_all_projects_results"


# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]


def persist_data_to_db(data, log):
    # collection = db[collection_name]
    try:
        data_id = collection.insert_one(data).inserted_id
        print("Successfully persisted data at ID: ", data_id, log)
    except Exception as e:
        print("Failed to persist data: ", e)


def load_json_to_mongodb():
    # Iterate over all JSON files in the specified directory
    for index, filename in enumerate(os.listdir(JSON_DIRECTORY), start=1):
        if filename.endswith(".json"):
            filepath = os.path.join(JSON_DIRECTORY, filename)
            with open(filepath, "r") as file:
                try:
                    data = json.load(file)
                    # # Insert data into MongoDB
                    # collection.insert_one(data)
                    print(
                        f" {index} =================================== ================= GETTING DATA FOR ================================================ {filename}"
                    )
                    restructure_data(data)
                    print(f"Inserted data from {filename} into MongoDB")
                except json.JSONDecodeError:
                    print(f"Failed to decode JSON from file {filename}")


def restructure_data(data):
    commits = data.get("commits", None)
    if commits:
        total_commits = len(commits)
        for commit_index, commit in enumerate(commits, start=1):
            print_log = f"-------------------------- {commit_index}/{total_commits}"

            repo = commit["repository"]
            commit_id = commit["sha1"]
            repo_fullname, repo_name = extract_repo_parts(repo)

            refactorings = commit.get("refactorings", [])
            if refactorings:
                for ref_index, refactoring in enumerate(refactorings, start=1):
                    refactoring["project"] = repo_name
                    refactoring["commitId"] = commit_id
                    persist_data_to_db(refactoring, print_log)
            else:
                no_ref = {}
                no_ref["project"] = repo_name
                no_ref["commitId"] = commit_id
                no_ref["type"] = None
                no_ref["description"] = None
                no_ref["leftSideLocations"] = []
                no_ref["rightSideLocations"] = []
                persist_data_to_db(no_ref, print_log)


def extract_repo_parts(url):
    # Remove the .git suffix
    clean_url = re.sub(r"\.git$", "", url)

    # Extract the "user/repo" part
    user_repo_match = re.search(r"github\.com/([^/]+/[^/]+)", clean_url)
    user_repo = user_repo_match.group(1) if user_repo_match else None

    # Extract the repository name
    repo_match = re.search(r"github\.com/[^/]+/([^/]+)", clean_url)
    repo_name = repo_match.group(1) if repo_match else None

    return user_repo, repo_name


if __name__ == "__main__":
    load_json_to_mongodb()
