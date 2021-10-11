from gedutil.mongo_client import families


def get_parents_from_doc(fam, combined=True):
    if combined:
        res = []
        for key in ["wife", "husb"]:
            if key in fam:
                res.extend(fam[key])
        return res
    else:
        res = {}
        for key in ["husb", "wife"]:
            if key in fam:
                res[key] = fam[key]
        return res


def get_parent_info(fam_id, combined=True):
    assert isinstance(fam_id, str)
    fam = families.find_one({"fam_id": fam_id}, {"wife": 1, "husb": 1})
    return get_parents_from_doc(fam, combined)
