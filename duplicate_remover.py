from pymongo import MongoClient

# Replace the following with your MongoDB connection details
client = MongoClient("mongodb://localhost:27017/")
db = client["first-research"]

# Replace these with your actual collection names
collection1 = db["java-projects"]
collection2 = db["java-projects-20stars"]


def remove_duplicates_based_on_name():
    # Fetch all documents from both collections
    documents_collection1 = list(collection1.find({}, {"_id": 0, "name": 1}))
    documents_collection2 = list(collection2.find({}, {"_id": 0, "name": 1}))

    # Extract the 'name' field values
    names_collection1 = {doc["name"] for doc in documents_collection1}
    names_collection2 = {doc["name"] for doc in documents_collection2}

    # Find common names (duplicates)
    common_names = names_collection1.intersection(names_collection2)

    # Remove duplicates from collection2 based on 'name' field
    if common_names:
        collection2.delete_many({"name": {"$in": list(common_names)}})
        print(f"Removed {len(common_names)} duplicates from collection2.")
    else:
        print("No duplicates found.")


if __name__ == "__main__":
    remove_duplicates_based_on_name()
