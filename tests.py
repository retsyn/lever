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
    testing_mesh2 = cmds.polyCube()[0]
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

    # Testing rig-spec:
    new_expression = rigspec.Expression(
        "placer: p=(12, 38, 2), n=hellow, c=yellow, type=1"
    )

    # Testing Matrices
    test_matrix = matrices.lmatrix(testing_mesh)
    test_matrix2 = matrices.lmatrix(testing_mesh2)
    test_suite.assert_near(
        test_matrix.trans,
        cmds.xform(testing_mesh, q=True, t=True, ws=True),
        0.1,
        "Testing if matrix trans property matches actual transform.",
    )
    print(test_matrix.trans)
    print(cmds.xform(testing_mesh, q=True, t=True, ws=True))

    # Rotate the testing meshes in predicted and random orientations for vector tests.
    cmds.rotate(90, 0, 0, testing_mesh)
    random_rot = random_vector()
    cmds.rotate(random_rot[0], random_rot[1], random_rot[2], testing_mesh2)
    rot_matrix = matrices.lmatrix(testing_mesh)
    test_suite.assert_true(
        rot_matrix.x_vector == (1.0, 0.0, 0.0),
        "Testing x_vector member of lmatrix is unchanged.",
    )

    test_suite.assert_true(
        rot_matrix.y_vector == (0.0, 0.0, 1.0),
        "Testing x_vector member of lmatrix points scene-forward.",
    )

    test_suite.assert_true(
        rot_matrix.z_vector == (0.0, -1.0, 0.0),
        "Testing z_vector member of lmatrix points scene-down.",
    )

    # Apply the matrix taken from testing_mesh2 to testing_mesh1
    test_matrix2.apply(testing_mesh)

    test_suite.assert_near(
        cmds.xform(testing_mesh, q=True, t=True, ws=True),
        cmds.xform(testing_mesh2, q=True, t=True, ws=True),
        0.0001,
        "Testing if the application of the same matrix has placed it in an identical spot.",
    )

    print(f"{rot_matrix.x_vector}")
    print(f"{rot_matrix.y_vector}")
    print(f"{rot_matrix.z_vector}")

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

    # TODO
    # Tests for apply matrix.

    # Test for aim-at.

    test_suite.report()
    print("Remember that an unclean scene make cause failures.")
