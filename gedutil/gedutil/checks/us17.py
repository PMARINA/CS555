from gedutil.base import ID, Error_Type, User_Story
from gedutil.mongo_client import errors, families

from .check import Check
from .utils.get_fam_info import get_child_ids_from_doc, get_parents_from_doc


class US17(Check):
    """
    Assignment:

    > Parents should not marry any of their descendants

    """

    def __init__(self):
        pass

    def setup(self):  # pragma: no cover
        pass

    def run(self):
        family_collection = []
        # Go through the families
        for doc in families.find():
            parents = get_parents_from_doc(doc)
            child_ids = get_child_ids_from_doc(doc)
            if not (parents and child_ids):
                continue
            family_collection.append(
                (doc[ID.FAM_ID.name], set(parents), set(child_ids))
            )
        for doc in families.find():
            spouses = set(get_parents_from_doc(doc))
            if not spouses:
                continue
            for fam_id, parents, children in family_collection:
                parents_in_doc = False
                children_in_doc = False
                for parent in parents:
                    if parent in spouses:
                        parents_in_doc = True
                        break
                for child in children:
                    if child in spouses:
                        children_in_doc = True
                        break
                if parents_in_doc and children_in_doc:
                    err_msg = (
                        f"A parent and their child (from family ID: {fam_id}) were listed as spouses"
                        f" in a family (family ID: {doc[ID.FAM_ID.name]})"
                    )
                    errors.insert_one(
                        {
                            "user story": User_Story.US17.name,
                            "error type": Error_Type.ERROR.name,
                            "message": err_msg,
                        }
                    )
