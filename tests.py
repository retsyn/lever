"""
tests.py
Created: Friday, 1st September 2023 9:31:20 am
Matthew Riche
Last Modified: Friday, 1st September 2023 9:31:26 am
Modified By: Matthew Riche
"""

# This doesn't employ python's comfy 'unittest' module due to the fact that unittest.TestCase's
# output doesn't appear in the maya script editor.  We use "munittest", a module I made to get
# around stuff like this.

import maya.cmds as cmds
import sys

import random

sys.path.append("C:/3DDev/rtech/")

try:
    print("Importing local copy of munittest")
    from munittest import m_unit_test as munit
except:
    raise ImportError(
        "munittest not available.  Get it at https://github.com/retsyn/munittest"
    )


from . import build
from . import lvnode
from . import placer


def random_vector():
    """Generate randomized coordinates in space for robust testing.

    Returns:
        tuple: Random euler vector
    """
    x = random.uniform(-1000000.0, 1000000.0)
    y = random.uniform(-1000000.0, 1000000.0)
    z = random.uniform(-1000000.0, 1000000.0)

    return (x, y, z)


def full_suite_test():
    test_suite = munit.SuiteUnitTest()

    #  Testing lvNode
    testing_mesh = cmds.polyCube()[0]
    lv_test_node = lvnode.LvNode(testing_mesh)

    test_position = random_vector()
    print(test_position)
    lv_test_node.translate = test_position
    test_suite.assert_near(
        lv_test_node.translate,
        test_position,
        0.00001,
        f"Testing lvnode translate property is readable and settable.",
    )

    # Test build object, creation and properties.
    test_position = random_vector()
    gen_build_object = build.BuildObject(test_position)
    test_suite.assert_equal(
        str(gen_build_object),
        "Lever Build object called Generic Build Object.  Type: UNKNOWN.",
        "Testing output string.",
    )
    test_suite.assert_node_exists("Dud", "Testing that a Dud was created...")
    test_suite.assert_node_type(
        gen_build_object.shape, "mesh", "Testing that Dud is the correct node type."
    )

    test_suite.assert_near(
        gen_build_object.translation,
        test_position,
        0.000001,
        f"Testing Dud is at point {test_position}",
    )
    test_suite.assert_equal(
        gen_build_object.translation, list(test_position), "Testing property getter."
    )

    test_position = random_vector()
    gen_build_object.translation = test_position
    test_suite.assert_equal(
        gen_build_object.translation, list(test_position), "Testing property setter."
    )
    test_suite.assert_near(
        gen_build_object.translation,
        test_position,
        0.000001,
        "Testing Dud has moved to new point via setter.",
    )

    # Test placer
    test_position = random_vector()
    test_size = random.uniform(0.1, 9.9)
    test_placer_object = placer.Placer(test_position, test_size, "test_placer")
    test_suite.assert_node_exists(
        test_placer_object.trans, "Testing that a single placer node exists."
    )
    test_suite.assert_node_type(
        test_placer_object.shape, "nurbsSurface", "Testing Placer type is nurbsSurface"
    )
    test_suite.assert_near(
        test_placer_object.translation,
        test_position,
        0.0001,
        "Testing translation getter on placer.",
    )
    test_position = random_vector()
    test_placer_object.translation = test_position
    test_suite.assert_near(
        test_placer_object.translation,
        test_position,
        0.00001,
        "Testing Placer object translation setter.",
    )
    test_suite.assert_equal(
        cmds.getAttr(test_placer_object.trans + ".scaleX"), test_size,
        "Asserting that assigned size applied to placer trans",
    )

    test_suite.report()
    print("Remember that an unclean scene make cause failures.")
