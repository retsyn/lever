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
import pprint as pp


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
    from . import build
except:
    raise ImportError("Couldn't parse build module")

try:
    from . import lvnode
except:
    raise ImportError("Couldn't parse lvnode module")

try:
    from . import placer
except:
    raise ImportError("Couldn't parse placer module.")

try:
    from . import rigspec
except:
    raise ImportError("Couldn't parse rigspec module.")

try:
    from . import transforms
except:
    raise ImportError("Couldn't parse transforms module.")


class build_objects_suite(munit.SuiteUnitTest):

    def test_lvnode_translate(self):
        # Testing lvNode translate properties.
        testing_mesh = cmds.polyCube()[0]
        lv_test_node = lvnode.LvNode(testing_mesh)
        test_position = random_vector()
        lv_test_node.translate = test_position
        self.assert_near(lv_test_node.translate, test_position, 0.00001)
        lv_test_node.delete_node()

    def test_lvnode_delete(self):
        #  Testing lvNode deletion
        testing_mesh = cmds.polyCube()[0]
        lv_deletion_test = lvnode.LvNode(testing_mesh)
        name_str = lv_deletion_test.name
        lv_deletion_test.delete_node()
        self.assert_node_not_exists(name_str)

    def test_generic_build_object_str(self):
        # Testing generic build object str method
        test_position = random_vector()
        gen_build_object = build.PlanObject(test_position)
        self.assertEqual(
            str(gen_build_object),
            "Lever Build object called Generic Build Object.  Type: UNKNOWN."
        )

    def test_dud_build(self):
        test_position = random_vector()
        gen_build_object = build.PlanObject(test_position)
        self.assert_node_exists(gen_build_object.name)

    def test_build_create(self):
        # Test build object, creation and properties.
        test_position = random_vector()
        gen_build_object = build.PlanObject(test_position)
        self.assert_node_exists(gen_build_object.name)
        
        test_suite.assert_node_type(
            gen_build_object.shape, "mesh", "Testing that Dud is the correct node type."
        )
        
def random_vector(rot=False):
    """Generate randomized coordinates in space for robust testing.

    Returns:
        tuple: Random euler vector
    """

    if rot == False:
        lower_bound = -1000000.0
        upper_bound = 1000000.0
    else:
        lower_bound = -360.0
        upper_bound = 360.0

    x = random.uniform(lower_bound, upper_bound)
    y = random.uniform(lower_bound, upper_bound)
    z = random.uniform(lower_bound, upper_bound)

    return (x, y, z)


class build_objects_suite(munit.SuiteUnitTest):

  


def build_objects_test():
    """Tests of LvNode, Generic Build Objects, and Placer system.

    Args:
        test_suite (_type_): _description_
    """


    # Test build object, creation and properties.
    test_position = random_vector()
    gen_build_object = build.PlanObject(test_position)
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

    # Test the cleanup features:
    build.PlanObject.clean_all()

    test_suite.assert_false(
        cmds.objExists(test_placer_object.trans),
        f"Asserting that {test_placer_object.trans} is deleted.",
    )
    test_suite.assert_false(
        cmds.objExists(gen_build_object.trans),
        f"Asserting that {gen_build_object.trans} is deleted.",
    )

    cmds.delete(testing_mesh)


def rigspec_test(testsuite: munit.SuiteUnitTest):
    """Testing the unit test module.

    Args:
        testsuite (munit.SuiteUnitTest): Ongoing test suite
    """

    # Rigspec might look like:
    #"placer: p=(12, 38, 2), n=wrist, c=yellow, type=1"
    #" > placer: p=(12, 38, 2), n=finger1, c=yellow, type=1"
    #" > > placer: p=(12, 38, 2), n=finger2, c=yellow, type=1""
    #" > placer: p=(12, 38, 2), n=thumb, c=yellow, type=1"

    # Testing rig-spec:
    new_expression = rigspec.Expression(
        "placer: p=(12, 38, 2), n=hello, c=yellow, type=1"
    )
    new_expression.breakdown()

def orientation_test(testsuite: munit.SuiteUnitTest):
    aim_locator = lvnode.LvNode(cmds.spaceLocator(n="aim_at_me")[0])
    up_locator = lvnode.LvNode(cmds.spaceLocator(n="im_up")[0])
    subject_locator = lvnode.LvNode(cmds.spaceLocator(n="im_aiming")[0])

    cmds.xform(aim_locator.name, t=(10, 10, 0), ws=True)
    cmds.xform(up_locator.name, t=(0, 0, 10), ws=True)

    transforms.aim_at(subject_locator, aim_locator, up_locator)
    testsuite.assert_near(
        subject_locator.rotate,
        (-45.0, -90.0, 0.0),
        0.0001,
        "Did temp aim constraint orient as expected with default yxz order.",
    )
    transforms.aim_at(subject_locator, aim_locator, up_locator, primary_axis='z', secondary_axis='y')
    testsuite.assert_near(
        subject_locator.rotate,
        (90.0, 0.0, 135.0),
        0.0001,
        "Did temp aim constraint orient as expected with zyx order..",
    )
    transforms.aim_at(subject_locator, aim_locator, up_locator, primary_axis='x', secondary_axis='z')
    testsuite.assert_near(
        subject_locator.rotate,
        (0.0, 0.0, 45.0),
        0.0001,
        "Did temp aim constraint orient as expected with xzy order.",
    )

def full_suite_test():
    """Full Test of all modules."""
    
    # Create a test suite that automatically discovers all test cases
    #suite = munit.unittest.defaultTestLoader.loadTestsFromModule(__name__)
    suite = munit.unittest.defaultTestLoader.loadTestsFromTestCase(build_objects_suite)

    # Create a test runner
    runner = munit.unittest.TextTestRunner()

    # Run the test suite
    runner.run(suite)
