from datetime import timedelta

from dateutil.parser import parse as parseDate

from gedutil.base import ID, GED_Tag
from gedutil.mongo_client import families, individuals

from check import Check
from utils.get_fam_info import get_parents_from_doc


class US06(Check):
    def __init__(self):
        pass

    def setup(self):  
        pass

    def run(self):

        # Go through the families
        for doc in families.find():
            ids_of_people = get_parents_from_doc(doc)
            if GED_Tag.BIRT.name not in doc:
                continue
            birt_date = parseDate(doc[GED_Tag.BIRT.name])
            
            for id in ids_of_people:
                person = individuals.find_one({ID.IND_ID.name: id})
                if GED_Tag.DEAT.name not in person:
                    f"This person does not have a recorded death date."
                    continue
                deat_date = parseDate(person[GED_Tag.DEAT.name])
                yearsAlive = deat_date - birt_date
                if yearsAlive > 150:
                    raise ValueError(
                        f"US07 - {person} was alive for more than 150 years."
                    )