"""
vectors.py
Created: Saturday, 29th July 2023 2:42:55 pm
Matthew Riche
Last Modified: Sunday, 24th September 2023 5:06:00 pm
Modified By: Matthew Riche
"""


# This module leverages MVector from om2 to provide vector math that is strong against FPP errors.

from maya.api.OpenMaya import MVector
import maya.cmds as cmds
import logging as log
import decimal as dc
from typing import Union
from .console import dprint
from .lvnode import LvNode

dc.getcontext().prec = 32


class LVector:
    def __init__(self, vector: iter):
        """A wrapper of mvector for simple access outside.

        Args:
            vector (iter): an iterable containing 3 floats.  Will be sanitized if values are wrong.
        """
        self.mvector = MVector()
        self._sanitize(vector)

    def _sanitize(self, vector: Union[iter, MVector]):
        """Throws errors if values aren't a proper 3 element vector.

        Args:
            vector (iter): An interable.

        Raises:
            TypeError: If anything inside the iterable isn't a usable number.
            ValueError: If the number of elements isn't exactly 3.
        """
        if isinstance(vector, (list, tuple)):
            for v in vector:
                if isinstance(v, (float, int, dc.Decimal)) == False:
                    raise TypeError(f"{v} must be a float or int, not {type(v)}.")
            if len(vector) != 3:
                raise ValueError(f"{vector} doesn't have the right number of elements.")
            self.mvector = MVector(vector)

        elif isinstance(vector, LVector):
            self.mvector = MVector(
                (vector.precise_x, vector.precise_y, vector.precise_z)
            )
        elif isinstance(vector, MVector):
            self.mvector = vector
        else:
            raise TypeError(
                f"Provided vector to sanitize was {type(vector)} which is unhandled."
            )

    def cross_prod(self, vector2: iter):
        """Calculate cross product between this vector an another given vector.

        Args:
            vector2 (iter): Any iterable representing (x, y, z).

        Returns:
            MVector: A new MVector value.
        """
        self._sanitize(vector2)
        vector2 = MVector(vector2)
        cross_prod = self.mvector ^ vector2

        return LVector(cross_prod)

    def dot_prod(self, vector2: iter):
        """Calculate the do

        Args:
            vector2 (iter): _description_

        Returns:
            float: _description_
        """
        self._sanitize(vector2)

        return LVector(self.mvector * vector2)

    def normalize(self):
        self.mvector.normalize()
        self.x = self.mvector.x
        self.y = self.mvector.y
        self.z = self.mvector.z

    @property
    def x(self) -> float:
        return self.mvector.x

    @x.setter
    def x(self, value):
        if isinstance(value, (float, int, dc.Decimal)) == False:
            raise TypeError(f"{value} needs to be int or float.")
        self.mvector.x = value

    @property
    def precise_x(self) -> dc.Decimal:
        return dc.Decimal(self.mvector.x)

    @property
    def y(self) -> float:
        return self.mvector.y

    @y.setter
    def y(self, value):
        if isinstance(value, (float, int, dc.Decimal)) == False:
            raise TypeError(f"{value} needs to be int or float.")
        self.mvector.y = value

    @property
    def precise_y(self) -> dc.Decimal:
        return dc.Decimal(self.mvector.y)

    @property
    def z(self) -> float:
        return self.mvector.z

    @z.setter
    def z(self, value):
        if isinstance(value, (float, int, dc.Decimal)) == False:
            raise TypeError(f"{value} needs to be int or float.")
        self.mvector.z = value

    @property
    def precise_z(self) -> dc.Decimal:
        return dc.Decimal(self.mvector.z)

    def __add__(self, vector2):
        """For adding other vectors

        Args:
            vector2 (iter): vector or iterable (will be sanitized)
        """
        vector2 = self._sanitize(vector2)

        return LVector(
            (
                self.mvector.x + vector2.x,
                self.mvector.y + vector2.y,
                self.mvector.z + vector2.z,
            )
        )

    def __sub__(self, vector2: iter):
        """For subtracting other vectors.

        Args:
            vector2 (iter): vector or iterable (will be sanitized)
        """
        vector2 = LVector(vector2)

        return LVector(
            (
                self.mvector.x - vector2.x,
                self.mvector.y - vector2.y,
                self.mvector.z - vector2.z,
            )
        )

    def __len__(self) -> int:
        """A len method to satisfy certain vector sanitization checks.
        This will be a hard 3 if this class is doing it's job.

        Returns:
            int: Always 3.
        """
        return 3
    
    def __str__(self) -> str:
        return (f"LVector(({self.x}, {self.y}, {self.z}))")

    def __getitem__(self, index: int) -> float:
        """When indexed, we expose whichever element of the mvector inside.

        Args:
            index (int): _description_

        Raises:
            IndexError: If the index isn't 0,1,2 aligning with x,y,z.

        Returns:
            float: The x, y, or z content of the MVector.
        """
        if index == 0:
            return self.mvector.x
        elif index == 1:
            return self.mvector.y
        elif index == 2:
            return self.mvector.z
        else:
            raise IndexError(f"Can't get index {index}, must be 0,1,2 for x,y,z.")


def plane_normal(point_a: iter, point_b: iter, point_c: iter) -> LVector:
    """Get a normal angle from a plane defined by three points.

    Args:
        point_a (iterable): Point A comprised by plane
        point_b (iterable): Point B comprised by plane
        point_c (iterable): Point C comprised by plane

    Returns:
        MVector: Line vector normal of the plane.
    """

    point_a = LVector(point_a)
    point_b = LVector(point_b)
    point_c = LVector(point_c)

    return (point_c - point_a) * (point_b - point_c)


def best_fit_from_plane():
    pass
    # TODO
    """
        # Initialize plane normal
    norm = OpenMaya.MVector()
    
    # Get Point Positions
    ptList = [glTools.utils.base.getPosition(p) for p in ptList]
    
    # Calculate Plane Normal
    for i in range(len(ptList)):
        prev = OpenMaya.MVector(ptList[i-1][0],ptList[i-1][1],ptList[i-1][2])
        curr = OpenMaya.MVector(ptList[i][0],ptList[i][1],ptList[i][2])
        norm += OpenMaya.MVector((prev.z + curr.z) * (prev.y - curr.y), (prev.x + curr.x) * (prev.z - curr.z), (prev.y + curr.y) *  (prev.x - curr.x))
    
    # Normalize result
    norm.normalize()
    """


def get_line(point_a: iter, point_b: iter, reversed=False) -> LVector:
    """Get a single vector represting the line vector.

    Args:
        point_a (iterable): First point on the line.
        point_b (iterable): End point on the line.
        reversed (bool, optional): To give the reversed line. Defaults to False.

    Returns:
        MVector: A line vector
    """

    point_a = LVector(point_a)
    point_b = LVector(point_b)
    if reversed:
        return point_b - point_a
    else:
        return point_a - point_b
