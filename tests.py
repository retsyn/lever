"""
tests.py
Created: Friday, 1st September 2023 9:31:20 am
Matthew Riche
Last Modified: Friday, 1st September 2023 9:31:26 am
Modified By: Matthew Riche
"""

# This doens't employ python's comfy 'unittest' module due to the fact that unittest.TestCase's
# output doesn't appear in the maya script editor.  A manual solution instead.

import sys
sys.path.append("C:/3DDev/rtech/")

try:
    print("Importing local copy of munittest")
    from munittest import m_unit_test as munit
except:
    raise ImportError("munittest not available.  Get it at https://github.com/retsyn/munittest")


from . import build


def full_suite_test():
    test_suite = munit.SuiteUnitTest()

    # Test build object
    gen_build_object = build.BuildObject((666.0, 666.0, 666.0))
    test_suite.assert_equal(
        str(gen_build_object),
        "Lever Build object called Generic Build Object.  Type: UNKNOWN.", "Testing output string."
    )

    gen_build_object.build()
    test_suite.assert_node_exists("Dud", "Testing that a Dud was created...")


    test_suite.report()
