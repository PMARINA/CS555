from datetime import timedelta

from dateutil.parser import parse as parseDate

from gedutil.base import ID, GED_Tag
from gedutil.mongo_client import families, individuals

from .check import Check
from .utils.get_fam_info import get_parents_from_doc


class US25(Check):
    def __init__(self):
        pass

    def setup(self):  # pragma: no cover
        pass

    def run(self):
        for doc in families.find({}, {ID.FAM_ID.name: 1, GED_Tag.CHIL.name: 1}):
            if GED_Tag.CHIL.name in doc:
                children_ids = doc[GED_Tag.CHIL.name]
                children = set()
                for id in children_ids:
                    child_doc = individuals.find_one(
                        {ID.IND_ID.name: id},
                        {"_id": 0, GED_Tag.NAME.name: 1, GED_Tag.BIRT.name: 1},
                    )
                    child = None
                    if (
                        GED_Tag.NAME.name in child_doc
                        and GED_Tag.BIRT.name in child_doc
                    ):
                        child = (
                            child_doc[GED_Tag.NAME.name],
                            child_doc[GED_Tag.BIRT.name],
                        )
                    elif GED_Tag.NAME.name in child_doc:
                        child = child_doc[GED_Tag.NAME.name]
                    elif GED_Tag.BIRT.name in child_doc:
                        child = child_doc[GED_Tag.BIRT.name]
                    else:
                        pass
                        # raise Exception(child_doc) # The child has neither a name nor a birth date
                    if child in children:
                        raise ValueError(
                            f"Duplicate child in family {doc[ID.FAM_ID.name]}: {child}"
                        )
                    else:
                        children.add(child)
