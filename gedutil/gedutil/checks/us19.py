from gedutil.base import ID, Error_Type, GED_Tag, User_Story
from gedutil.mongo_client import errors, families

from .check import Check
from .utils.get_fam_info import get_child_ids_from_doc, get_parents_from_doc


class US19(Check):
    """
    Assignment:

    > First cousins should not marry one another

    """

    def __init__(self):
        pass

    def setup(self):  # pragma: no cover
        pass

    def run(self):
        cousin_groups = []
        # Go through the families
        for doc in families.find():
            child_ids = get_child_ids_from_doc(doc)
            family_cousins = []
            if not child_ids:
                continue
            for child in child_ids:
                for child_doc in families.find(
                    {"$or": [{GED_Tag.HUSB.name: child}, {GED_Tag.WIFE.name: child}]}
                ):
                    grand_children = get_child_ids_from_doc(child_doc)
                    if grand_children:
                        family_cousins.extend(grand_children)
            if len(family_cousins) >= 1:
                cousin_groups.append((doc[ID.FAM_ID.name], set(family_cousins)))
        for doc in families.find():
            spouses = set(get_parents_from_doc(doc))
            if not spouses:
                continue
            for fam_id, cousins in cousin_groups:
                num_spouses_from_family = 0
                for cousin in cousins:
                    if cousin in spouses:
                        num_spouses_from_family += 1
                    if num_spouses_from_family > 1:
                        break
                if num_spouses_from_family > 1:
                    err_msg = (
                        f"Multiple cousins (from family ID: {fam_id}) were listed as spouses"
                        f" in a family (family ID: {doc[ID.FAM_ID.name]})"
                    )
                    errors.insert_one(
                        {
                            "user story": User_Story.US19.name,
                            "error type": Error_Type.ERROR.name,
                            "message": err_msg,
                        }
                    )
