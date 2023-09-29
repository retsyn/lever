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
    from . import matrices
except:
    raise ImportError("Couldn't parse matrices module.")

try:
    from . import vectors
except:
    raise ImportError("Couldn't parse Vectors module.")


def random_vector():
    """Generate randomized coordinates in space for robust testing.

    Returns:
        tuple: Random euler vector
    """
    x = random.uniform(-1000000.0, 1000000.0)
    y = random.uniform(-1000000.0, 1000000.0)
    z = random.uniform(-1000000.0, 1000000.0)

    return (x, y, z)


def build_objects_test(test_suite):
    """Tests of LvNode, Generic Build Objects, and Placer system.

    Args:
        test_suite (_type_): _description_
    """

    #  Testing lvNode, translate properties.
    testing_mesh = cmds.polyCube()[0]
    lv_test_node = lvnode.LvNode(testing_mesh)
    test_position = random_vector()
    lv_test_node.translate = test_position
    test_suite.assert_near(
        lv_test_node.translate,
        test_position,
        0.00001,
        f"Testing lvnode translate property is readable and settable.",
    )

    # Test build object, creation and properties.
    test_position = random_vector()
    gen_build_object = build.PlanObject(test_position)
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

    # Testing rig-spec:
    new_expression = rigspec.Expression(
        "placer: p=(12, 38, 2), n=hellow, c=yellow, type=1"
    )
    # TODO put in tests for each value of the expression.


def matrices_test(test_suite: munit.SuiteUnitTest()):
    """Testing LMatrix class

    Args:
        test_suite (munit.SuiteUnitTest): _description_
    """

    testing_mesh = cmds.polyCube(n="test_mesh_a")[0]
    testing_mesh2 = cmds.polyCube(n="test_mesh_b")[0]
    test_spot = random_vector()
    # Testing Matrices
    cmds.xform(testing_mesh, t=test_spot, ws=True)
    test_matrix = matrices.LMatrix(testing_mesh)
    print(
        f"Matrix.trans of {testing_mesh} after random movement:\n{str(test_matrix.trans)}"
    )
    test_suite.assert_near(
        test_matrix.trans,
        cmds.xform(testing_mesh, q=True, t=True, ws=True),
        0.1,
        "Testing if matrix trans property matches actual transform.",
    )

    # Rotate the testing meshes in predicted and random orientations for vector tests.
    cmds.rotate(90, 0, 0, testing_mesh)
    print("Rotated the test_mesh.")
    random_rot = random_vector()
    rot_matrix = matrices.LMatrix(testing_mesh)
    print(f"Reading x_vector of {testing_mesh} as {rot_matrix.x_vector}")
    test_suite.assert_true(
        rot_matrix.x_vector == (1.0, 0.0, 0.0),
        "Testing x_vector member of lmatrix is unchanged.",
    )

    print(f"Reading y_vector of {testing_mesh} as {rot_matrix.y_vector}")
    test_suite.assert_true(
        rot_matrix.y_vector == (0.0, 0.0, 1.0),
        "Testing y_vector member of lmatrix points scene-forward.",
    )

    print(f"Reading z_vector of {testing_mesh} as {rot_matrix.z_vector}")
    test_suite.assert_true(
        rot_matrix.z_vector == (0.0, -1.0, 0.0),
        "Testing z_vector member of lmatrix points scene-down.",
    )

    cmds.rotate(random_rot[0], random_rot[1], random_rot[2], testing_mesh2)
    test_matrix2 = matrices.LMatrix(testing_mesh2)

    # Apply the matrix taken from testing_mesh2 to testing_mesh1
    test_matrix2.apply_to_transform(testing_mesh)

    test_suite.assert_near(
        cmds.xform(testing_mesh, q=True, t=True, ws=True),
        cmds.xform(testing_mesh2, q=True, t=True, ws=True),
        0.0001,
        "Testing if the application of the same matrix has placed it in an identical translation.",
    )

    test_suite.assert_near(
        cmds.xform(testing_mesh, q=True, ro=True, ws=True),
        cmds.xform(testing_mesh2, q=True, ro=True, ws=True),
        0.0001,
        "Testing if the application of the same matrix has placed it in an identical orientation.",
    )

    # Test for aim-at.
    test_subject = lvnode.LvNode(cmds.spaceLocator(n="test_subject")[0])
    aim_target = lvnode.LvNode(cmds.spaceLocator(n="aim_at_me")[0])
    secondary_target = lvnode.LvNode(cmds.spaceLocator(n="seconary_aim")[0])
    aim_target.translate = (10, 10, 0)
    secondary_target.translate = (0, 0, -10)

    aimed_matrix = matrices.LMatrix(test_subject)
    print(f"{aimed_matrix.x_vector}\n{aimed_matrix.y_vector}\n{aimed_matrix.z_vector}")
    aimed_matrix.aim(test_subject, aim_target, secondary_target)

    aimed_matrix.apply_to_transform(test_subject)

    print("Remember that an unclean scene make cause failures.")


def vectors_test(test_suite: munit.SuiteUnitTest):
    x_rand = random.uniform(-1000, 1000)
    y_rand = random.uniform(-1000, 1000)
    z_rand = random.uniform(-1000, 1000)

    print(f"Testing with values x:{x_rand}, y:{y_rand}, z:{z_rand}")
    new_vec = vectors.LVector((x_rand, y_rand, z_rand))
    print(f"x:{new_vec.x}, y:{new_vec.y}, z:{new_vec.z}")
    test_suite.assert_equal(
        x_rand, new_vec.x, f"Does attribute value of {new_vec.x} match {x_rand}"
    )

    x_b = random.uniform(-1000, 1000)
    y_b = random.uniform(-1000, 1000)
    z_b = random.uniform(-1000, 1000)

    print(f"Testing athrithmetic with values x:{x_b}, y:{y_b}, z:{z_b}")
    b_vec = vectors.LVector((x_b, y_b, z_b))
    neg_vec = new_vec - b_vec

    test_suite.assert_equal(
        neg_vec.x,
        (new_vec.x - b_vec.x),
        f"x attribute correctly resolving to {neg_vec.x}",
    )

    test_suite.assert_equal(
        neg_vec.y,
        (new_vec.y - b_vec.y),
        f"y attribute correctly resolving to {neg_vec.y}",
    )

    test_suite.assert_equal(
        neg_vec.z,
        (new_vec.z - b_vec.z),
        f"z attribute correctly resolving to {neg_vec.z}",
    )

    # Get Line test.



def full_suite_test():
    """Full Test of all modules."""
    test_suite = munit.SuiteUnitTest()

    # build_objects_test(test_suite)
    # rigspec_test(test_suite)
    # vectors_test(test_suite)
    matrices_test(test_suite)

    test_suite.report()
