"""
vector.py
Created: Friday, 30th June 2023 10:58:39 am
Matthew Riche
Last Modified: Friday, 30th June 2023 10:58:39 am
Modified By: Matthew Riche
"""


# This module leverages MVector from om2 to provide vector math that is strong against FPP errors.

from maya.api.OpenMaya import MVector
import maya.cmds as cmds
import logging as log


class lvector:
    def __init__(self, vector: iter):
        self._sanitize(vector)
        self.mvector = vector

    def _sanitize(self, vector: iter):
        for v in vector:
            if isinstance(v, (float, int) == False):
                raise TypeError(f"{v} must be a float or int, not {type(v)}.")
        if len(vector != 3):
            raise ValueError(f"{vector} doesn't have the right number of elements.")

    def cross_prod(self, vector2: iter) -> MVector:
        self._sanitize(vector2)
        cross_prod = self.mvector ^ vector2

        return cross_prod

    def dot_prod(self, vector2: iter) -> float:
        self._sanitize(vector2)

        return self.mvector * vector2

    @property
    def x(self) -> float:
        return self.mvector.x

    @x.setter
    def x(self, value):
        if isinstance(value, (float, int)):
            raise TypeError(f"{value} needs to be int or float.")
        self.mvector.x = value

    @property
    def y(self) -> float:
        return self.mvector.y

    @y.setter
    def y(self, value):
        if isinstance(value, (float, int)):
            raise TypeError(f"{value} needs to be int or float.")
        self.mvector.y = value

    @property
    def z(self) -> float:
        return self.mvector.z

    @z.setter
    def z(self, value):
        if isinstance(value, (float, int)):
            raise TypeError(f"{value} needs to be int or float.")
        self.mvector.z = value

    def __add__(self, vector2):
        """For adding other vectors

        Args:
            vector2 (iter): vector or iterable (will be sanitized)
        """
        vector2 = self._sanitize(vector2)

        return MVector(
            self.mvector.x + vector2.x,
            self.mvector.y + vector2.y,
            self.mvector.z + vector2.z
        )


    def __sub__(self, vector2: iter):
        """For subtracting other vectors.

        Args:
            vector2 (iter): vector or iterable (will be sanitized)
        """
        vector2 = self._sanitize(vector2)

        return MVector(
            self.mvector.x - vector2.x,
            self.mvector.y - vector2.y,
            self.mvector.z - vector2.z
        )

def plane_normal(point_a: iter, point_b: iter, point_c: iter) -> MVector:
    """Get a normal angle from a plane defined by three points.

    Args:
        point_a (iterable): Point A comprised by plane
        point_b (iterable): Point B comprised by plane
        point_c (iterable): Point C comprised by plane

    Returns:
        MVector: Line vector normal of the plane.
    """

    point_a = lvector(point_a)
    point_b = lvector(point_b)
    point_c = lvector(point_c)

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


def get_line(point_a: iter, point_b: iter, reversed=False) -> MVector:
    """Get a single vector represting the line vector.

    Args:
        point_a (iterable): First point on the line.
        point_b (iterable): End point on the line.
        reversed (bool, optional): To give the reversed line. Defaults to False.

    Returns:
        MVector: A line vector
    """

    point_a = lvector(point_a)
    point_b = lvector(point_b)
    if reversed:
        return point_b - point_a
    else:
        return point_a - point_b
