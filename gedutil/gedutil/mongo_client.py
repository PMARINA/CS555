from pymongo import MongoClient

from .config import DATABASE_NAME, FAMILIES_COLLECTION_NAME, INDIVIDUALS_COLLECTION_NAME

client = MongoClient()


our_db = client.get_database(DATABASE_NAME)
individuals = our_db.get_collection(INDIVIDUALS_COLLECTION_NAME)
families = our_db.get_collection(FAMILIES_COLLECTION_NAME)


def get_db(name=DATABASE_NAME):
    global our_db
    our_db = client.get_database(name)
    return our_db


def get_individuals(name=INDIVIDUALS_COLLECTION_NAME):
    global individuals
    individuals = get_db().get_collection(name)
    return individuals


def get_families(name=FAMILIES_COLLECTION_NAME):
    global families
    families = get_db().get_collection(name)
    return families


def reset_database():
    client.drop_database(DATABASE_NAME)
    get_db()
    get_individuals()
    get_families()
