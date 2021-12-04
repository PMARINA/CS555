# comment
from datetime import datetime
from typing import *

from dateutil.parser import parse as parse_date

from gedutil.base import ID, Error_Type, GED_Tag, User_Story
from gedutil.mongo_client import errors, families, individuals

from .check import Check
from .utils.get_fam_info import get_parents_from_doc


class US11(Check):
    def __init__(self):
        pass

    def setup(self):  # pragma: no cover
        pass

    def run(self):
        # Go through the families
        for doc in individuals.find():
            current_marriage: Optional[Tuple[datetime, datetime]] = None
            marriage_ranges: List[Tuple[datetime, datetime]] = []
            individual_id = doc[ID.IND_ID.name]
            individual_death_date = (
                parse_date(doc[GED_Tag.DEAT.name])
                if GED_Tag.DEAT.name in doc
                else datetime.max
            )
            families_with_individual = families.find(
                {
                    "$or": [
                        {GED_Tag.WIFE.name: individual_id},
                        {GED_Tag.HUSB.name: individual_id},
                    ]
                }
            )
            families_with_individual = [f for f in families_with_individual]
            for fam in families_with_individual:
                marr: List[Optional[datetime], Optional[datetime]] = [
                    None,
                    individual_death_date,
                ]
                if GED_Tag.MARR.name in fam:
                    marr[0] = parse_date(fam[GED_Tag.MARR.name])
                if GED_Tag.DIV.name in fam:
                    marr[1] = parse_date(fam[GED_Tag.DIV.name])
                other_partners = get_parents_from_doc(fam)
                other_partners.remove(individual_id)
                for partner_id in other_partners:
                    inner_doc = individuals.find_one({ID.IND_ID.name: partner_id})
                    if GED_Tag.DEAT.name in inner_doc:
                        marriage_end_date_string = inner_doc[GED_Tag.DEAT.name]
                        marriage_end_date = parse_date(marriage_end_date_string)
                        if marr[1]:
                            marr[1] = min(
                                [individual_death_date, marr[1], marriage_end_date]
                            )
                        else:
                            marr[1] = marriage_end_date
                curr_marr_tuple = (marr[0], marr[1])
                marriage_ranges.append(curr_marr_tuple)
            zipped = list(zip(marriage_ranges, families_with_individual))
            zipped = sorted(zipped, key=lambda t: t[0][0])
            marriage_ranges = [t[0] for t in zipped]
            families_with_individual = [t[1] for t in zipped]
            end_of_last_marriage = None
            bigamy = False
            current_bigamy = False
            for i, m in enumerate(marriage_ranges):
                if not end_of_last_marriage:
                    end_of_last_marriage = m[1] if m[1] else datetime.max
                else:
                    if m[0] < end_of_last_marriage:
                        if end_of_last_marriage > datetime.now():
                            current_bigamy = True
                        bigamy = True
                        break
                    end_of_last_marriage = m[1] if m[1] else datetime.max
            if bigamy and not current_bigamy:
                errors.insert_one(
                    {
                        "user story": User_Story.US11.name,
                        "error type": Error_Type.ERROR.name,
                        "message": f"Individual ({individual_id}) has been in 2+ concurrent marriages ({families_with_individual[i-1][ID.FAM_ID.name]}, {families_with_individual[i][ID.FAM_ID.name]}) in the past",
                    }
                )
                break
            elif bigamy and current_bigamy:
                errors.insert_one(
                    {
                        "user story": User_Story.US11.name,
                        "error type": Error_Type.ERROR.name,
                        "message": f"Individual ({individual_id}) is currently in 2+ concurrent marriages ({families_with_individual[i-1][ID.FAM_ID.name]}, {families_with_individual[i][ID.FAM_ID.name]})",
                    }
                )
                break
