import os
from dataclasses import dataclass
from enum import Enum, auto
from typing import *

import regex as re
from loguru import logger

verbose = False
if not verbose:
    logger.disable(__name__)


class GED_Tag(Enum):
    INDI = auto()
    NAME = auto()
    SEX = auto()
    BIRT = auto()
    DEAT = auto()
    FAMC = auto()
    FAMS = auto()
    FAM = auto()
    MARR = auto()
    HUSB = auto()
    WIFE = auto()
    CHIL = auto()
    DIV = auto()
    DATE = auto()
    HEAD = auto()
    TRLR = auto()
    NOTE = auto()


@dataclass(frozen=True)
class GED_Line:
    __slots__ = "level", "tag", "args"
    level: int
    tag: Union[GED_Tag, str]
    args: str

    def is_valid(self):
        return not isinstance(self.tag, str)


class Parser:
    def __init__(self, GED_Input: str):
        ged_input_string = ""
        if os.path.exists(GED_Input):
            GED_Input = os.path.abspath(GED_Input)
            logger.debug(f"Detected file input to GED_Parser: {GED_Input}")
            with open(GED_Input) as f:
                ged_input_string = f.read()
        else:
            ged_input_string = GED_Input
        self.raw_input = ged_input_string
        self.raw_input_lines = ged_input_string.splitlines()

    def parse(self):
        self.parsed_lines = []
        regex_type1 = re.compile(
            r"^([0-2])\s(INDI|NAME|SEX|BIRT|DEAT|FAMC|FAMS|FAM|MARR|HUSB|WIFE|CHIL|DIV|DATE|HEAD|TRLR|NOTE)\s(.*)$"
        )
        regex_type2 = re.compile(r"^([0-2])\s(.*?)\s(INDI|FAM)$")
        regex_type3 = re.compile(r"^([0-9]).*?([_A-Z]{3,6})\s(.*)$")
        regex_type4 = re.compile(r"^([0-9]).*?(.*)\s([_A-Z]{3,6})$")
        for line in self.raw_input_lines:
            match1 = regex_type1.match(line)
            if match1:
                # Follows format number, tag, stuff
                level = match1.group(1)
                tag = match1.group(2)
                args = match1.group(3)
            else:
                match2 = regex_type2.match(line)
                if match2:
                    # Follows format number, stuff, tag
                    level = match2.group(1)
                    args = match2.group(2)
                    tag = match2.group(3)
                    pass
                else:
                    # Format unrecognized... maybe need to debug?
                    match3 = regex_type3.match(line)
                    if match3:
                        level = match3.group(1)
                        tag = match3.group(2)
                        args = match3.group(3)
                    else:
                        match4 = regex_type4.match(line)
                        if match4:
                            level = match4.group(1)
                            args = match4.group(2)
                            tag = match4.group(3)
                        else:
                            logger.error(line)
                            continue
            if match1 or match2 or tag in GED_Tag.__members__:
                tag = GED_Tag[tag]
            parsed_line: GED_Line = GED_Line(level, tag, args.strip())
            self.parsed_lines.append(parsed_line)

    def print_input_output_project_2_assignment(self):
        for i in range(len(self.raw_input_lines)):
            print(f"--> {self.raw_input_lines[i]}")
            o = self.parsed_lines[i]
            Y = "Y"
            N = "N"
            print(
                f"<-- {o.level}|{o.tag.name if o.is_valid() else o.tag}|{Y if o.is_valid() else N}|{o.args}"
            )
