"""
test_build.py
Created: Sunday, 1st September 2024 3:37:20 pm
Matthew Riche
Last Modified: Sunday, 1st September 2024 3:37:54 pm
Modified By: Matthew Riche
"""

import sys
from ..sundry import random_vector

sys.path.append("C:/3DDev/rtech/")

try:
    print("Importing local copy of munittest")
    from munittest import m_unit_test as munit
except:
    raise ImportError(
        "munittest not available.  Get it at https://github.com/retsyn/munittest"
    )


print("Importing modules.")
try:
    from .. import build
except:
    raise ImportError("Couldn't parse build module")


class build_objects_suite(munit.SuiteUnitTest):

    def test_generic_build_object_str(self):
        # Testing generic build object str method
        test_position = random_vector()
        gen_build_object = build.PlanObject(test_position)
        self.assertEqual(
            str(gen_build_object),
            f"Lever Build object called {gen_build_object.name}.  Type: UNKNOWN.",
        )

    def test_dud_build(self):
        test_position = random_vector()
        gen_build_object = build.PlanObject(test_position)
        self.assert_node_exists(gen_build_object.trans)

    def test_dud_type(self):
        test_position = random_vector()
        gen_build_object = build.PlanObject(test_position)
        self.assert_node_type(gen_build_object.trans, "transform")

    def test_dud_location(self):
        test_position = random_vector()
        gen_build_object = build.PlanObject(test_position)
        self.assert_near(gen_build_object.translation, test_position, 0.0001)

    def test_trans_property(self):
        test_position = random_vector()
        translate_position = random_vector()
        gen_build_object = build.PlanObject(test_position)
        gen_build_object.translation = translate_position
        self.assert_near(gen_build_object.translation, translate_position, 0.0001)
