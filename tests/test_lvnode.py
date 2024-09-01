'''
test_lvnode.py
Created: Sunday, 1st September 2024 3:34:50 pm
Matthew Riche
Last Modified: Sunday, 1st September 2024 3:35:45 pm
Modified By: Matthew Riche
'''

import maya.cmds as cmds
import sys
from ..sundry import random_vector
from .. import transforms


sys.path.append("C:/3DDev/rtech/")

try:
    print("Importing local copy of munittest")
    from munittest import m_unit_test as munit
except:
    raise ImportError(
        "munittest not available.  Get it at https://github.com/retsyn/munittest"
    )

try:
    from .. import lvnode
except:
    raise ImportError("Couldn't parse lvnode module")


class lvnode_suite(munit.SuiteUnitTest):

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



# Turn this into a test class soon:
'''
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
'''