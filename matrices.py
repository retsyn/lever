"""
matrices.py
Created: Sunday, 17th September 2023 7:55:08 pm
Matthew Riche
Last Modified: Sunday, 17th September 2023 7:55:11 pm
Modified By: Matthew Riche
"""

import maya.cmds as cmds
import maya.api.OpenMaya as om2
import decimal as dc
from . import vectors
from .lvnode import LvNode
from .console import dprint
from typing import Union


dc.getcontext().prec = 32


class LMatrix:
    def __init__(self, node: Union[str, LvNode]):
        if isinstance(node, str):
            if cmds.objExists(node) == False:
                raise ValueError(f"{node} isn't found in the scene or is not unique.")
            elif cmds.nodeType(node) not in ["transform", "joint"]:
                raise TypeError(
                    f"{node} is not a type that has a transform, so can't make a Matrix."
                )
            node_name = node
        elif isinstance(node, LvNode):
            dprint(f"Converting {node} to just {node.name}")
            node_name = node.name

        dprint(f"Making a matrix for the node {node_name}")
        sel_list = om2.MGlobal.getSelectionListByName(node_name)
        transform_dag = sel_list.getDagPath(0)
        transform_fn = om2.MFnTransform(transform_dag)

        self.matrix = transform_fn.transformation()

    def _as_mmatrix(self) -> om2.MMatrix:
        """Convert to om2.MMatrix, which has more low-level access.

        Returns:
            om2.MMatrix: The MMatrix with the mutable elements.
        """
        return self.matrix.asMatrix()

    @property
    def x_vector(self) -> tuple:
        matrix = self._as_mmatrix()
        return (matrix[0], matrix[1], matrix[2])

    @x_vector.setter
    def x_vector(self, value: iter):
        matrix = self._as_mmatrix()
        for val in value:
            if isinstance(val, (float, int, dc.Decimal)) == False:
                raise TypeError(f"{val} is not a float or int.")

        if len(value) != 3:
            raise ValueError(f"{value} doesn't contain exactly three values.")

        matrix[0] = value[0]
        matrix[1] = value[1]
        matrix[2] = value[2]

        self.matrix = om2.MTransformationMatrix(matrix)

    @property
    def y_vector(self) -> tuple:
        matrix = self._as_mmatrix()
        return (matrix[4], matrix[5], matrix[6])

    @y_vector.setter
    def y_vector(self, value: iter):
        matrix = self._as_mmatrix()
        for val in value:
            if isinstance(val, (float, int, dc.Decimal)) == False:
                raise TypeError(f"{val} is not a float or int.")

        if len(value) != 3:
            raise ValueError(f"{value} doesn't contain exactly three values.")

        matrix[4] = value[4]
        matrix[5] = value[5]
        matrix[6] = value[6]

        self.matrix = om2.MTransformationMatrix(matrix)

    @property
    def z_vector(self) -> tuple:
        matrix = self._as_mmatrix()
        return (matrix[8], matrix[9], matrix[10])

    @z_vector.setter
    def z_vector(self, value: iter):
        matrix = self._as_mmatrix()
        for val in value:
            if isinstance(val, (float, int, dc.Decimal)) == False:
                raise TypeError(f"{val} is not a float or int.")

        if len(value) != 3:
            raise ValueError(f"{value} doesn't contain exactly three values.")

        matrix[8] = value[8]
        matrix[9] = value[9]
        matrix[10] = value[10]

        self.matrix = om2.MTransformationMatrix(matrix)

    @property
    def trans(self):
        return vectors.LVector((self.matrix.translation(om2.MSpace.kWorld)))

    @trans.setter
    def trans(self, value: iter):
        self.matrix.setTranslation(om2.MVector(value), om2.MSpace.kWorld)

    def __getitem__(self, i):
        matrix = self._as_mmatrix()
        return matrix[i]

    def __setitem__(self, i, value):
        matrix = self._as_mmatrix
        matrix[i] = value

    def aim(
        self,
        subject: Union[str, LvNode],
        primary_target: Union[str, LvNode],
        secondary_target: Union[str, LvNode],
        primary_axis="y",
        secondary_axis="x",
    ):
        """Will 'aim' a matrix at a target object, and orient it's secondary axis to another
        object.

        Args:
            subject (str): The object to aim.
            primary_target (str): The target object to aim at.
            secondary_target (str): The target object to align the secondary axis to.
            primary_axis (str, optional): Which axis should be aimed. Defaults to "y".
            secondary_axis (str, optional): Which axis should be secondary. Defaults to "x".

        Raises:
            ValueError: If one of the targets does not exist.
            TypeError: If one of the targets isn't a transform or joint.
            ValueError: If one of the axis isn't described by an appropriate letter.
            ValueError: If the primary and secondary axis are the same.
        """

        if(isinstance(subject, LvNode)):
            subject = subject.name
        if(isinstance(primary_target, LvNode)):
            primary_target = primary_target.name
        if(isinstance(secondary_target, LvNode)):
            secondary_target = secondary_target.name

        for node_name in [subject, primary_target, secondary_target]:
            if cmds.objExists(node_name) == False:
                raise ValueError(
                    f"{node_name} doesn't exist in the scene or is not unique."
                )
            if cmds.objectType(node_name) not in ["transform", "joint"]:
                raise TypeError(f"{node_name} not of type joint or transform.")

        for axis_value in [primary_axis, secondary_axis]:
            if axis_value not in ["x", "y", "z"]:
                raise ValueError(
                    f"primary and secondary axis must be 'x', 'y', or 'z', not {axis_value}."
                )

        if secondary_axis == primary_axis:
            raise ValueError(
                f"Primary and secondary axis were both {primary_axis}.  The need to differ."
            )

        # Calculate normalized line vector between subject and target
        pos_a = vectors.LVector(cmds.xform(subject, q=True, t=True, ws=True))
        pos_b = vectors.LVector(cmds.xform(primary_target, q=True, t=True, ws=True))
        primary_vector = vectors.get_line(pos_a, pos_b)
        primary_vector.normalize()

        # Calculate normalized line vector between subject and secondary axis target
        pos_c = vectors.LVector(cmds.xform(secondary_target, q=True, t=True, ws=True))
        secondary_vector = vectors.get_line(pos_a, pos_c)
        secondary_vector.normalize()

        # Derive tertiary axis
        tertiary_vector = primary_vector.cross_prod(secondary_vector)
        tertiary_vector.normalize()

        # 'Sanitize' secondary vector:
        secondary_vector = primary_vector.cross_prod(tertiary_vector)
        secondary_vector.normalize()

        # Set the matrix content
        unused_axis = ["x", "y", "z"]
        # Match case not available in this Mayapy.
        # The aimed vector in the primary chosen axis:
        if primary_axis == "x":
            self.x_vector = primary_vector
            unused_axis.remove("x")
        elif primary_axis == "y":
            self.y_vector = primary_vector
            unused_axis.remove("y")
        elif primary_axis == "z":
            self.z_vector = primary_vector
            unused_axis.remove("z")

        # The 'up' vector (secondary axis) in chosen secondary axis.
        if secondary_axis == "x":
            self.x_vector = secondary_vector
            unused_axis.remove("x")
        elif secondary_axis == "y":
            self.y_vector = secondary_vector
            unused_axis.remove("y")
        elif secondary_axis == "z":
            self.z_vector = secondary_vector
            unused_axis.remove("z")

        if unused_axis[0] == "x":
            self.x_vector = tertiary_vector
        elif unused_axis[0] == "y":
            self.y_vector = tertiary_vector
        elif unused_axis[0] == "z":
            self.z_vector = tertiary_vector

    def apply_to_transform(self, node_name: str):
        """Applies the transformation defined by this matrix.

        Args:
            node_name (str): A unique node name in the scene.

        Raises:
            NameError: If the name doesn't exist in the scene (or is not unique.)
            TypeError: If the node named isn't an appropriate transform.
        """
        if cmds.objExists(node_name) == False:
            raise NameError(f"{node_name} not found in scene or is not unique.")
        if cmds.objectType(node_name) not in ["transform", "joint"]:
            raise TypeError(
                f"{node_name} is type {cmds.objectType(node_name)}, must be transform or joint."
            )

        sel = om2.MSelectionList()
        sel.add(node_name)
        dag_path = sel.getDagPath(0)

        transform_fn = om2.MFnTransform(dag_path)
        transform_fn.setTransformation(self.matrix)
