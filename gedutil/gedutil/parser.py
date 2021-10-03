import os

import regex as re
from loguru import logger

from .base import GED_Line, GED_Tag
from .hooks.birt import Birt
from .hooks.chil import Chil
from .hooks.date import Date
from .hooks.deat import Deat
from .hooks.div import Div
from .hooks.fam import Fam
from .hooks.famc import Famc
from .hooks.fams import Fams
from .hooks.husb import Husb
from .hooks.indi import Indi
from .hooks.marr import Marr
from .hooks.name import Name
from .hooks.sex import Sex
from .hooks.wife import Wife
from .mongo_client import reset_database

verbose = False
if not verbose:
    logger.disable(__name__)


class Parser:

    hooks = {
        GED_Tag.INDI: Indi(),
        GED_Tag.NAME: Name(),
        GED_Tag.SEX: Sex(),
        GED_Tag.DATE: Date(),
        GED_Tag.BIRT: Birt(),
        GED_Tag.DEAT: Deat(),
        GED_Tag.FAM: Fam(),
        GED_Tag.FAMC: Famc(),
        GED_Tag.FAMS: Fams(),
        GED_Tag.MARR: Marr(),
        GED_Tag.DIV: Div(),
        GED_Tag.HUSB: Husb(),
        GED_Tag.WIFE: Wife(),
        GED_Tag.CHIL: Chil(),
    }

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

    def read(self):
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
                level = int(match1.group(1))
                tag = match1.group(2)
                args = match1.group(3)
            else:
                match2 = regex_type2.match(line)
                if match2:
                    # Follows format number, stuff, tag
                    level = int(match2.group(1))
                    args = match2.group(2)
                    tag = match2.group(3)
                    pass
                else:
                    # Format unrecognized... maybe need to debug?
                    match3 = regex_type3.match(line)
                    if match3:
                        level = int(match3.group(1))
                        tag = match3.group(2)
                        args = match3.group(3)
                    else:
                        match4 = regex_type4.match(line)
                        if match4:
                            level = int(match4.group(1))
                            args = match4.group(2)
                            tag = match4.group(3)
                        else:
                            logger.error(line)
                            continue
            if match1 or match2 or tag in GED_Tag.__members__:
                tag = GED_Tag[tag]
            parsed_line: GED_Line = GED_Line(level, tag, args.strip())
            self.parsed_lines.append(parsed_line)

    def parse(self):
        reset_database()
        current_level = -1
        structure = []
        last_is_valid = False
        structure_is_valid = False
        for line in self.parsed_lines:
            if line.level <= current_level:
                structure = structure[: line.level + 1]
                structure[line.level] = line.tag
            else:
                structure.append(line.tag)
            current_level = line.level
            structure_is_valid = all([type(i) != str for i in structure])
            if line.tag in self.hooks:
                self.hooks[line.tag].process(line, structure_is_valid)
                last_is_valid = True
            else:
                last_is_valid = False

    def print_input_output_project_2_assignment(self):
        for i in range(len(self.raw_input_lines)):
            print(f"--> {self.raw_input_lines[i]}")
            o = self.parsed_lines[i]
            Y = "Y"
            N = "N"
            print(
                f"<-- {o.level}|{o.tag.name if o.is_valid() else o.tag}|{Y if o.is_valid() else N}|{o.args}"
            )
