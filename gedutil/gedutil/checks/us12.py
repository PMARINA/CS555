from gedutil.mongo_client import families, individuals

from .check import Check
from .utils.get_fam_info import get_child_ids_from_doc, get_parents_from_doc
from .utils.individuals import get_age, get_birthdate, isFemale, isMale


class US12(Check):
    """
    Assignment:

    > Mother should be less than 60 years older than her children and father should be less than 80 years older than his children

    """

    MAX_M_AFAB_AGE = 80
    MAX_F_AFAB_AGE = 60

    def __init__(self):
        pass

    def setup(self):  # pragma: no cover
        pass

    def run(self):

        # Go through the families
        for doc in families.find():
            parent_ids = get_parents_from_doc(doc)
            child_ids = get_child_ids_from_doc(doc)
            if (not child_ids) or (not parent_ids):
                # Either children or parents are not present = no parsing...
                continue
            child_birth_dates = {c: get_birthdate(c) for c in child_ids}
            parent_birth_dates = {p: get_birthdate(p) for p in parent_ids}
            for child_id in child_ids:
                child_bd = child_birth_dates[child_id]
                for parent_id in parent_ids:
                    parent_bd = parent_birth_dates[parent_id]
                    age_timedelta = get_age(parent_id, child_bd)
                    age_years = age_timedelta.days / 365.25
                    if isMale(parent_id):
                        if age_years > self.MAX_M_AFAB_AGE:
                            raise ValueError(
                                f"Male AFAB parent ({parent_id}) was more than {self.MAX_M_AFAB_AGE} years older ({age_years} years) than child at birth ({child_id})"
                            )
                    if isFemale(parent_id):
                        if age_years > self.MAX_F_AFAB_AGE:
                            raise ValueError(
                                f"Female AFAB parent ({parent_id}) was more than {self.MAX_F_AFAB_AGE} years older ({age_years} years) than child at birth ({child_id})"
                            )
