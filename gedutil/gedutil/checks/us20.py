from dataclasses import dataclass
from datetime import timedelta
from typing import List

from dateutil.parser import parse as parseDate

from gedutil.base import ID, Error_Type, GED_Tag, User_Story
from gedutil.mongo_client import errors, families, individuals

from .check import Check
from .utils.get_fam_info import get_child_ids_from_doc, get_parents_from_doc
from .utils.individuals import isFemale


@dataclass
class Family:
    parents: List[str]
    children: List[str]


class US20(Check):
    def __init__(self):
        pass

    def setup(self):  # pragma: no cover
        pass

    def run(self):
        def get_grandchildren(id_of_gen1_children, fams):
            for f in fams:
                if id_of_gen1_children in f.parents:
                    return f.children

        families_output = []
        spouses = set()

        for doc in families.find():
            parents = get_parents_from_doc(doc)
            child_ids = get_child_ids_from_doc(doc)
            families_output.append(Family(parents, child_ids))
            if parents[0] > parents[1]:
                spouses.add((parents[0], parents[1]))
            else:
                spouses.add((parents[1], parents[0]))

        for family in families_output:
            children = family.children
            if not children:
                continue  # There are no grandchildren to evaluate
            all_grandchildren = []
            for c_id in children:
                s = get_grandchildren(c_id, families_output)
                if s:
                    all_grandchildren.extend(s)
            for c in children:
                for g in all_grandchildren:
                    if (g, c) in spouses or (c, g) in spouses:
                        errors.insert_one(
                            {
                                "user story": User_Story.US20.name,
                                "error type": Error_Type.ANOMALY.name,
                                "message": f"An uncle/parent/aunt ({c}) was in a family with a child of the next generation ({g})",
                            }
                        )
