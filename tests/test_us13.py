import unittest

from gedutil import US13, Error_Type, GED_Line, GED_Tag, Parser, User_Story, errors

from .path_util import stabilize


class TestUS13(unittest.TestCase):
    """
    Children Spacing
    Fam ID: F6000000178632944866

    CHIL:
     @I6000000178633610873@             12 JAN 1977
     @I6000000178633463852@             11 JAN 1977 OR 4 OCT 1975 OR 11 FEB 1977 (depending on the test)
    """

    def test_bad_spacing(self):
        u = US13()
        path = stabilize("US13", "bad_spacing")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        num_raised = 0
        for doc in errors.find():
            assert doc["user story"] == User_Story.US13.name
            assert doc["error type"] == Error_Type.ERROR.name
            num_raised += 1
        assert num_raised == 1

    def test_valid_close(self):
        u = US13()
        path = stabilize("US13", "control_close")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        for doc in errors.find():
            raise Exception("An error should not have been raised")

    def test_valid_far(self):
        u = US13()
        path = stabilize("US13", "control")
        p = Parser(path)
        p.read()
        p.parse()
        u.run()
        for doc in errors.find():
            raise Exception("An error should not have been raised")
