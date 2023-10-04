"""
matrices.py
Created: Sunday, 17th September 2023 7:55:08 pm
Matthew Riche
Last Modified: Sunday, 17th September 2023 7:55:11 pm
Modified By: Matthew Riche
"""

import maya.cmds as cmds
import decimal as dc
from .console import dprint
from typing import Union
import math

dc.getcontext().prec = 17
epsilon = dc.Decimal('1e-5')


class LMatrix:
    def __init__(self, node=""):
        """A matrix class that leverages precise decimal values."""
        self.matrix = [
            [dc.Decimal(1.0), dc.Decimal(0.0), dc.Decimal(0.0), dc.Decimal(0.0)],
            [dc.Decimal(0.0), dc.Decimal(1.0), dc.Decimal(0.0), dc.Decimal(0.0)],
            [dc.Decimal(0.0), dc.Decimal(0.0), dc.Decimal(1.0), dc.Decimal(0.0)],
            [dc.Decimal(0.0), dc.Decimal(0.0), dc.Decimal(0.0), dc.Decimal(1.0)],
        ]

        if node != "":
            if isinstance(node, str):
                if cmds.objectType(node) in ["transform", "joint"]:
                    self.euler = cmds.xform(node, q=True, ro=True, ws=True)
                    self.translate = cmds.xform(node, q=True, t=True, ws=True)

    def _wrap_radians(self, rad) -> dc.Decimal:
        while rad <= -math.pi:
            rad += 2 * math.pi
            print(f"RAD increasing to {rad}")

        while rad > math.pi:
            rad -= 2 * math.pi
            print(f"RAD decreasing to {rad}")

        return rad

    def _3x3mult(self, matrix_a: list, matrix_b: list) -> list:
        """Multiplies 3x3 matrices (for calculating euler rotations)

        Args:
            matrix_a (list): 3x3 matrix (two dimensional list)
            matrix_b (list): 3x3 matrix (two dimensional list)

        Raises:
            ValueError: If the 3x3 Matrix isn't the right size.

        Returns:
            list: 2D list containing 3x3 Matrix.
        """

        # Guard corrupt input.
        if len(matrix_a) != 3 or len(matrix_b) != 3:
            raise ValueError(f"3x3mult only works on 3x3 matricies.")
        for i in range(3):
            if len(matrix_a[i]) != 3 or len(matrix_b[i]) != 3:
                raise ValueError(f"3x3mult only works on 3x3 matricies.")
            for j in range(3):
                if (
                    isinstance(matrix_a[i][j], (float, int, dc.Decimal)) == False
                    or isinstance(matrix_b[i][j], (float, int, dc.Decimal)) == False
                ):
                    raise TypeError(
                        f"Found that element [{i}][{j}] in one of the matrices isn't a number."
                    )

        # result matrix is all zeroes, since we will be multiplying on-top of it.
        result = [
            [dc.Decimal(0.0), dc.Decimal(0.0), dc.Decimal(0.0)],
            [dc.Decimal(0.0), dc.Decimal(0.0), dc.Decimal(0.0)],
            [dc.Decimal(0.0), dc.Decimal(0.0), dc.Decimal(0.0)],
        ]

        for i in range(3):
            for j in range(3):
                for k in range(3):
                    result[i][j] += dc.Decimal(matrix_a[i][k]) * dc.Decimal(
                        matrix_b[k][j]
                    )

        return result

    @property
    def x_vector_quant(self):
        return (self.matrix[0][0].quantize(epsilon, rounding=dc.ROUND_DOWN), 
                self.matrix[0][1].quantize(epsilon, rounding=dc.ROUND_DOWN), 
                self.matrix[0][2].quantize(epsilon, rounding=dc.ROUND_DOWN))
    
    @property
    def y_vector_quant(self):
        return (self.matrix[1][0].quantize(epsilon, rounding=dc.ROUND_DOWN), 
                self.matrix[1][1].quantize(epsilon, rounding=dc.ROUND_DOWN), 
                self.matrix[1][2].quantize(epsilon, rounding=dc.ROUND_DOWN))

    @property
    def z_vector_quant(self):
        return (self.matrix[2][0].quantize(epsilon, rounding=dc.ROUND_DOWN), 
                self.matrix[2][1].quantize(epsilon, rounding=dc.ROUND_DOWN), 
                self.matrix[2][2].quantize(epsilon, rounding=dc.ROUND_DOWN))

    @property
    def x_vector(self):
        return (self.matrix[0][0], self.matrix[0][1], self.matrix[0][2])
            
    @x_vector.setter
    def x_vector(self, vector: tuple):
        self.matrix[0][0] = vector[0]
        self.matrix[0][1] = vector[1]
        self.matrix[0][2] = vector[2]

    @property
    def y_vector(self):
        return (self.matrix[1][0], self.matrix[1][1], self.matrix[1][2])

    @y_vector.setter
    def y_vector(self, vector: tuple):
        self.matrix[1][0] = vector[0]
        self.matrix[1][1] = vector[1]
        self.matrix[1][2] = vector[2]

    @property
    def z_vector(self):
        return (self.matrix[2][0], self.matrix[2][1], self.matrix[2][2])

    @z_vector.setter
    def z_vector(self, vector: tuple):
        self.matrix[2][0] = vector[0]
        self.matrix[2][1] = vector[1]
        self.matrix[2][2] = vector[2]

    @property
    def translate(self) -> tuple:
        return (self.matrix[3][0], self.matrix[3][1], self.matrix[3][2])

    @translate.setter
    def translate(self, vector):
        self.matrix[3][0] = vector[0]
        self.matrix[3][1] = vector[1]
        self.matrix[3][2] = vector[2]

    @property
    def euler(self) -> tuple:
        """Calculate euler rotation defined by the matrix.

        Returns:
            tuple: Euler rotation (x, y, z)
        """
        rot_z = dc.Decimal(math.atan2(self.matrix[1][0], self.matrix[0][0]))
        rot_y = dc.Decimal(
            math.atan2(
                -self.matrix[2][0],
                math.sqrt(self.matrix[2][1] ** 2 + self.matrix[2][2] ** 2),
            )
        )
        rot_x = dc.Decimal(math.atan2(self.matrix[2][1], self.matrix[2][2]))

        # We need to wrap these radians.
        rot_x = self._wrap_radians(rot_x)
        rot_y = self._wrap_radians(rot_y)
        rot_z = self._wrap_radians(rot_z)

        # Convert from rad 2 deg
        rot_x = math.degrees(rot_x)
        rot_y = math.degrees(rot_y)
        rot_z = math.degrees(rot_z)

        # We keep the high precision Decimal type around during the math, but return basic floats.
        return (float(rot_x), float(rot_y), float(rot_z))

    @euler.setter
    def euler(self, vector: tuple):
        """Populates the matrix top 3x3 corner with vectors derived from euler angles.

        Args:
            vector (tuple): _description_
        """
        yaw = dc.Decimal(math.radians(vector[2]))
        pitch = dc.Decimal(math.radians(vector[1]))
        roll = dc.Decimal(math.radians(vector[0]))

        # Rotation about Z (yaw)
        R_z = [
            [math.cos(yaw), -math.sin(yaw), 0],
            [math.sin(yaw), math.cos(yaw), 0],
            [0, 0, 1],
        ]

        # Rotation about Y (pitch)
        R_y = [
            [math.cos(pitch), 0, math.sin(pitch)],
            [0, 1, 0],
            [-math.sin(pitch), 0, math.cos(pitch)],
        ]

        # Rotation about X (roll)
        R_x = [
            [1, 0, 0],
            [0, math.cos(roll), -math.sin(roll)],
            [0, math.sin(roll), math.cos(roll)],
        ]

        R_zy = self._3x3mult(R_z, R_y)
        R_zyx = self._3x3mult(R_zy, R_x)

        # Embedd the 3x3 into the corner of the 4x4.
        for i in range(3):
            for j in range(3):
                self.matrix[i][j] = R_zyx[i][j]

    def apply_to_transform(self, node: str):
        if cmds.objExists(node) == False:
            raise ValueError(f"{node} not found in scene or not unique.")
        cmds.xform(node, ro=self.euler, ws=True)
        cmds.xform(node, t=self.translate, ws=True)
