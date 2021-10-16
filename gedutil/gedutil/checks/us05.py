# comment
from datetime import timedelta

from dateutil.parser import parse as parseDate

from gedutil.base import ID, GED_Tag
from gedutil.mongo_client import families, individuals

from .check import Check
from .utils.get_fam_info import get_parents_from_doc


class US05(Check):
    def __init__(self):
        pass

    def setup(self):  # pragma: no cover
        pass

    def run(self):

        # Go through the families
        for doc in families.find():
            ids_of_people = get_parents_from_doc(doc)
            if GED_Tag.MARR.name not in doc:
                continue
            marriage_date = parseDate(doc[GED_Tag.MARR.name])
            # latest_birth_date = marriage_date - timedelta(days=365 * 14)
            for id in ids_of_people:
                person = individuals.find_one({ID.IND_ID.name: id})
                if GED_Tag.DEAT.name not in person:
                    f"This person does not have a recorded death date."
                    continue
                deat_date = parseDate(person[GED_Tag.DEAT.name])
                if deat_date < marriage_date:
                    raise ValueError(
                        f"US05 - {deat_date} occured before marriage on {marriage_date}."
                    )
