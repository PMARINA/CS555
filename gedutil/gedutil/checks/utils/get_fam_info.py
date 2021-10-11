from gedutil.base import ID, GED_Tag
from gedutil.mongo_client import families

NAMES_OF_PARENTS = [GED_Tag.WIFE.name, GED_Tag.HUSB.name]


def get_parents_from_doc(fam, combined=True):
    if combined:
        res = []
        for key in NAMES_OF_PARENTS:
            if key in fam:
                res.extend(fam[key])
        return res
    else:
        res = {}
        for key in NAMES_OF_PARENTS:
            if key in fam:
                res[key] = fam[key]
        return res


def get_parent_info(fam_id, combined=True):
    assert isinstance(fam_id, str)
    filter = {}
    for n in NAMES_OF_PARENTS:
        filter[n] = 1
    fam = families.find_one({ID.FAM_ID.name: fam_id}, filter)
    return get_parents_from_doc(fam, combined)
