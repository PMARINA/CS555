from datetime import timedelta

from dateutil.parser import parse as parseDate

from gedutil.base import ID, Error_Type, GED_Tag, User_Story
from gedutil.mongo_client import errors, families, individuals

from .check import Check
from .utils.get_fam_info import get_child_ids_from_doc, get_parents_from_doc
from .utils.individuals import get_age


class US33(Check):
    def __init__(self):
        pass

    def setup(self):  # pragma: no cover
        pass

    def run(self):
        orphans_by_id = {}
        for doc in families.find():
            fam_id = doc[ID.FAM_ID.name]
            if GED_Tag.CHIL.name in doc:
                # There are children so we need to check
                parent_ids = get_parents_from_doc(doc)
                parent_is_alive = False
                for id in parent_ids:
                    parent_doc = individuals.find_one(
                        {ID.IND_ID.name: id}, {GED_Tag.DEAT.name: 1}
                    )
                    if GED_Tag.DEAT.name not in parent_doc:
                        parent_is_alive = True
                        break
                if not parent_is_alive:
                    child_ids = get_child_ids_from_doc(doc)
                    for id in child_ids:
                        if get_age(id).days / 365.25 < 18:
                            errors.insert_one(
                                {
                                    "user story": User_Story.US33.name,
                                    "error type": Error_Type.RESULT.name,
                                    "message": f"Child with id ({id}) is an orphan of family ({fam_id})",
                                }
                            )
                            # if fam_id in orphans_by_id:
                            #     orphans_by_id[fam_id].append(id)
                            # else:
                            #     orphans_by_id[fam_id] = [id]
        return orphans_by_id
