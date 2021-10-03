from pymongo import MongoClient

client = MongoClient()

our_db = client.cs555_team11

individuals = our_db.individuals
families = our_db.families


def reset_database():
    our_db.drop_collection("individuals")
    our_db.drop_collection("families")
    individuals = our_db.create_collection("individuals")
    families = our_db.create_collection("families")
    individuals.create_index("ged_id")
    families.create_index("fam_id")


# if __name__ == "__main__":
# reset_database()
