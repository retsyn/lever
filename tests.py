"""
tests.py
Created: Friday, 1st September 2023 9:31:20 am
Matthew Riche
Last Modified: Friday, 1st September 2023 9:31:26 am
Modified By: Matthew Riche
"""

# This doens't employ python's comfy 'unittest' module due to the fact that unittest.TestCase's
# output doesn't appear in the maya script editor.  A manual solution instead.

import maya.cmds as cmds
from maya.api.OpenMaya import MVector

from . import build

global total_tests 
global passed_tests
global failed_tests

total_tests, passed_tests, failed_tests = [0, 0, 0]


# These assert functions might need to change later.
def maya_assert_true(test: bool, test_name: str) -> bool:
    global total_tests, passed_tests, failed_tests
    total_tests += 1
    if test:
        print(f"{test_name}: PASSED.")
        passed_tests += 1
    else:
        print(f"{test_name}: FAILED.")
        failed_tests += 1


def maya_assert_float(test: float, assert_value: float, test_name: str) -> bool:
    global total_tests, passed_tests, failed_tests
    total_tests += 1
    if test == assert_value:
        print(f"{test_name}: PASSED.")
        passed_tests += 1
    else:
        print(f"{test_name}: FAILED.")
        failed_tests += 1


def maya_assert_vector(test: MVector, assert_value: MVector, test_name: str) -> bool:
    global total_tests, passed_tests, failed_tests
    total_tests += 1
    if(test == assert_value):
        print(f"{test_name}: PASSED.")
        passed_tests += 1
    else:
        print(f"{test_name}: FAILED.")
        failed_tests += 1


def test_buildObject():
    test_object = build.BuildObject((0, 0, 0), "test_generic")
    # Raw build of test object should create a 'Dud'
    maya_assert_true(cmds.objExists("Dud"), "Testing presence of Dud build_object")

    print("-----------")
    print(f"Total tests ran: {total_tests}")
    print(f"{passed_tests} passed.")
    print(f"{failed_tests} failed.")
