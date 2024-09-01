"""
tests.py
Created: Friday, 1st September 2023 9:31:20 am
Matthew Riche
Last Modified: Friday, 1st September 2023 9:31:26 am
Modified By: Matthew Riche
"""

import sys

import random
import pprint as pp

from .tests import test_lvnode
from .tests import test_build


sys.path.append("C:/3DDev/rtech/")

try:
    print("Importing local copy of munittest")
    from munittest import m_unit_test as munit
except:
    raise ImportError(
        "munittest not available.  Get it at https://github.com/retsyn/munittest"
    )

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


class rigspec_suite(munit.SuiteUnitTest):

    def test_rigspec_test(testsuite: munit.SuiteUnitTest):
        """Testing the unit test module.

        Args:
            testsuite (munit.SuiteUnitTest): Ongoing test suite
        """

        # Rigspec might look like:
        # "placer: p=(12, 38, 2), n=wrist, c=yellow, type=1"
        # " > placer: p=(12, 38, 2), n=finger1, c=yellow, type=1"
        # " > > placer: p=(12, 38, 2), n=finger2, c=yellow, type=1""
        # " > placer: p=(12, 38, 2), n=thumb, c=yellow, type=1"

        # Testing rig-spec:
        new_expression = rigspec.Expression(
            "placer: p=(12, 38, 2), n=hello, c=yellow, type=1"
        )
        new_expression.breakdown()


def full_suite_test():
    """Full Test of all modules."""

    suite = munit.TestSuite()

    suite.addTests(munit.defaultTestLoader.loadTestsFromModule(test_lvnode))
    suite.addTests(munit.defaultTestLoader.loadTestsFromModule(test_build))

    runner = munit.TextTestRunner()
    runner.run(suite)
