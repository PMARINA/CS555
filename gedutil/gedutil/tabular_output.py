from datetime import datetime, timedelta

from dateutil import parser as dateParse
from dateutil.relativedelta import relativedelta as rd
from prettytable import PrettyTable

from .base import ID, Error_Type, GED_Tag
from .mongo_client import errors, families, individuals


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
            row.append(i[ID.IND_ID.name] if ID.IND_ID.name in i else "")
            row.append(i[GED_Tag.NAME.name] if GED_Tag.NAME.name in i else "")
            row.append(i[GED_Tag.SEX.name] if GED_Tag.SEX.name in i else "")
            row.append(i[GED_Tag.BIRT.name] if GED_Tag.BIRT.name in i else "")
            date_to_compare = (
                dateParse.parse(i[GED_Tag.DEAT.name])
                if GED_Tag.DEAT.name in i
                else datetime.now()
            )
            age = (
                (
                    rd(
                        dt1=date_to_compare, dt2=dateParse.parse(i[GED_Tag.BIRT.name])
                    ).years
                )
                if GED_Tag.BIRT.name in i
                else ""
            )
            row.append(age)
            row.append(False if GED_Tag.DEAT.name in i else True)
            row.append(i[GED_Tag.DEAT.name] if GED_Tag.DEAT.name in i else "")
            for field in [GED_Tag.FAMC.name, GED_Tag.FAMS.name]:
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
            row.append(f[ID.FAM_ID.name] if ID.FAM_ID.name in f else "")
            row.append(f[GED_Tag.MARR.name] if GED_Tag.MARR.name in f else "")
            row.append(f[GED_Tag.DIV.name] if GED_Tag.DIV.name in f else "")
            for field in [GED_Tag.HUSB.name, GED_Tag.WIFE.name]:
                if field in f:
                    if len(f[field]) > 1:
                        husbs = "{" + ", ".join(f[field]) + "}"
                        husbnames = []
                        for id in f[field]:
                            husbnames.append(
                                individuals.find_one({ID.IND_ID.name: id})[
                                    GED_Tag.NAME.name
                                ]
                            )
                        husbnames = "{ " + ", ".join(husbnames) + " }"
                    else:
                        husbs = f[field][0]
                        husbnames = individuals.find_one({ID.IND_ID.name: husbs})[
                            GED_Tag.NAME.name
                        ]
                else:
                    husbs = ""
                    husbnames = ""
                row.append(husbs)
                row.append(husbnames)
            chil = ["'" + i + "'" for i in f[GED_Tag.CHIL.name]]
            row.append(("{" + ", ".join(chil) + "}") if GED_Tag.CHIL.name in f else "")
            rows.append(row)

        rows.sort(key=lambda a: a[0])

        for row in rows:
            p.add_row(row)

        print(p)

    def print_outputs(self):
        if errors.count_documents({}) <= 0:
            return
        rows = []
        p = PrettyTable()
        p.title = "Outputs"
        p.field_names = ["User Story", "Type", "Message"]
        for doc in errors.find():
            row = []
            row.append(doc["user story"])
            row.append(doc["error type"])
            row.append(str(doc["message"]))
            rows.append(row)
        rows = sorted(rows, key=lambda l: l[0] + l[1])
        for row in rows:
            if len(row) != 3:
                print(row)
            p.add_row(row)
        print(p)
