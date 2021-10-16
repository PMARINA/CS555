from datetime import datetime, timedelta
from typing import Optional

from dateutil.parser import parse as parseDate

from gedutil.base import ID, GED_Tag
from gedutil.mongo_client import individuals


def get_birthdate_raw(id: str):
    doc = individuals.find_one(
        {ID.IND_ID.name: id}, {GED_Tag.DEAT.name: 1, GED_Tag.BIRT.name: 1}
    )
    if not GED_Tag.BIRT.name in doc:
        return None  # No birthdate found
    return doc[GED_Tag.BIRT.name]


def get_birthdate(id: str) -> Optional[datetime]:
    raw_result = get_birthdate_raw(id)
    if raw_result == None:
        return None
    return parseDate(raw_result)


def get_age(id: str, date: Optional[datetime]) -> Optional[timedelta]:
    if not date:
        date = datetime.now()
    doc = individuals.find_one(
        {ID.IND_ID.name: id}, {GED_Tag.DEAT.name: 1, GED_Tag.BIRT.name: 1}
    )
    if not GED_Tag.BIRT.name in doc:
        return None  # No birthdate = cannot calculate age
    birth_date = parseDate(doc[GED_Tag.BIRT.name])
    if GED_Tag.DEAT.name in doc:
        death_date = parseDate(doc[GED_Tag.DEAT.name])
        return max(death_date - birth_date, date - birth_date)
    else:
        return date - birth_date


def isMale(id: str) -> Optional[bool]:
    doc = individuals.find_one({ID.IND_ID.name: id}, {GED_Tag.SEX.name: 1})
    if GED_Tag.SEX.name not in doc:
        return None
    else:
        return doc[GED_Tag.SEX.name] == "M"


def isFemale(id: str) -> Optional[bool]:
    maleResult = isMale(id)
    if maleResult != None:
        return not maleResult
    return maleResult  # None
