import unittest

from gedutil import US01, GED_Line, GED_Tag, Parser

from .path_util import stabilize

TEST_FILE_PATH = stabilize("us01", "control")


class TestUS01(unittest.TestCase):
    """
    This user story is about dates after the current date... birth/death/divorce/marriage

    I'll be testing using my custom test case, but with changes made between the original and the test cases

    """

    def test_birth(self):
        u = US01()
        p = Parser(TEST_FILE_PATH)
        p.read()
        for i in range(len(p.parsed_lines)):
            if p.parsed_lines[i].tag == GED_Tag.BIRT:
                newDate = u.tomorrow.strftime("%d %b %Y").upper()
                orig = p.parsed_lines[i + 1]
                p.parsed_lines[i + 1] = GED_Line(orig.level, orig.tag, args=newDate)
                break
        p.parse()
        with self.assertRaises(ValueError):
            u.run()

    def test_death(self):
        u = US01()
        p = Parser(TEST_FILE_PATH)
        p.read()
        for i in range(len(p.parsed_lines)):
            if p.parsed_lines[i].tag == GED_Tag.DEAT:
                newDate = u.tomorrow.strftime("%d %b %Y").upper()
                orig = p.parsed_lines[i + 1]
                p.parsed_lines[i + 1] = GED_Line(orig.level, orig.tag, args=newDate)
                break
        p.parse()
        with self.assertRaises(ValueError):
            u.run()

    def test_divorce(self):
        u = US01()
        p = Parser(TEST_FILE_PATH)
        p.read()
        for i in range(len(p.parsed_lines)):
            if p.parsed_lines[i].tag == GED_Tag.MARR:
                ori = p.parsed_lines[i]
                p.parsed_lines[i] = GED_Line(ori.level, GED_Tag.DIV, ori.args)
                newDate = u.tomorrow.strftime("%d %b %Y").upper()
                orig = p.parsed_lines[i + 1]
                p.parsed_lines[i + 1] = GED_Line(orig.level, orig.tag, args=newDate)
                break
        p.parse()
        with self.assertRaises(ValueError):
            u.run()

    def test_marriage(self):
        u = US01()
        p = Parser(TEST_FILE_PATH)
        p.read()
        for i in range(len(p.parsed_lines)):
            if p.parsed_lines[i].tag == GED_Tag.MARR:
                newDate = u.tomorrow.strftime("%d %b %Y").upper()
                orig = p.parsed_lines[i + 1]
                p.parsed_lines[i + 1] = GED_Line(orig.level, orig.tag, args=newDate)
                break
        p.parse()
        with self.assertRaises(ValueError):
            u.run()

    def test_birth_nonsensical_date(self):
        u = US01()
        p = Parser(TEST_FILE_PATH)
        p.read()
        for i in range(len(p.parsed_lines)):
            if p.parsed_lines[i].tag == GED_Tag.BIRT:
                newDate = "totally not a date"
                orig = p.parsed_lines[i + 1]
                p.parsed_lines[i + 1] = GED_Line(orig.level, orig.tag, args=newDate)
                break
        p.parse()
        with self.assertRaises(ValueError):
            u.run()
