from datetime import datetime, timedelta

from dateutil import parser as dateParse
from dateutil.relativedelta import relativedelta as rd
from prettytable import PrettyTable

from .mongo_client import families, individuals


class Tabular_Output:
    def __init__(self):
        pass

    def print_individuals(self):
        p = PrettyTable()
        p.title = "Individuals"
        p.field_names = [
            "ID",
            "Name",
            "Gender",
            "Birthday",
            "Age",
            "Alive",
            "Death",
            "Child",
            "Spouse",
        ]
        rows = []
        for i in individuals.find():
            row = []
            row.append(i["ged_id"] if "ged_id" in i else "")
            row.append(i["name"] if "name" in i else "")
            row.append(i["sex"] if "sex" in i else "")
            row.append(i["birt"] if "birt" in i else "")
            date_to_compare = (
                dateParse.parse(i["deat"]) if "deat" in i else datetime.now()
            )
            age = (
                (rd(dt1=date_to_compare, dt2=dateParse.parse(i["birt"])).years)
                if "birt" in i
                else ""
            )
            row.append(age)
            row.append(False if "deat" in i else True)
            row.append(i["deat"] if "deat" in i else "")
            for field in ["famc", "fams"]:
                if field in i:
                    ids = []
                    for id in i[field]:
                        ids.append(f"'{id}'")
                    ids = ", ".join(ids)
                    ids = "{" + ids + "}"
                else:
                    ids = ""
                row.append(ids)
            rows.append(row)
        rows.sort(key=lambda a: a[0])
        for row in rows:
            p.add_row(row)
        print(p)

    def print_families(self):
        p = PrettyTable()
        p.title = "Families"
        p.field_names = [
            "ID",
            "Married",
            "Divorced",
            "Husband ID",
            "Husband Name",
            "Wife ID",
            "Wife Name",
            "Children",
        ]
        rows = []
        for f in families.find():
            row = []
            row.append(f["fam_id"] if "fam_id" in f else "")
            row.append(f["marr"] if "marr" in f else "")
            row.append(f["div"] if "div" in f else "")
            for field in ["husb", "wife"]:
                if field in f:
                    if len(f[field]) > 1:
                        husbs = "{" + ", ".join(f[field]) + "}"
                        husbnames = []
                        for id in f[field]:
                            husbnames.append(
                                individuals.find_one({"ged_id": id})["name"]
                            )
                        husbnames = "{ " + ", ".join(husbnames) + " }"
                    else:
                        husbs = f[field][0]
                        husbnames = individuals.find_one({"ged_id": husbs})["name"]
                else:
                    husbs = ""
                    husbnames = ""
                row.append(husbs)
                row.append(husbnames)
            chil = ["'" + i + "'" for i in f["chil"]]
            row.append(("{" + ", ".join(chil) + "}") if "chil" in f else "")
            rows.append(row)

        rows.sort(key=lambda a: a[0])

        for row in rows:
            p.add_row(row)

        print(p)
