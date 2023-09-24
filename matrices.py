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

dc.getcontext().prec = 32


class lmatrix:
    def __init__(self, node: str):
        """Given a transform node, return a MMatrix of it's position.

        Args:
            node (str): The name of the node.  Must exist and be unique.

        Raises:
            ValueError: If the node isn't found in scene or isn't unique.
            TypeError: If the node doesn't have transform properties.

        Returns:
            MMatrix: Usable matrix data (from om2.)
        """

        if cmds.objExists == False:
            raise ValueError(
                f"{node} isn't a node found in the scene (Or is not unique)."
            )
        elif cmds.objectType(node) not in ["joint", "transform"]:
            raise TypeError(f"{node} is not of type joint or transform.")

        # Get a dagpath in order toget a MFnTransform in order to return a MMatrix.
        selection_list = om2.MGlobal.getSelectionListByName(node)
        dag_path = selection_list.getDagPath(0)
        transform_fn = om2.MFnTransform(dag_path)

        self.mmatrix = transform_fn.transformation().asMatrix()

        self.x_vector = (
            dc.Decimal(self.mmatrix[0]),
            dc.Decimal(self.mmatrix[1]),
            dc.Decimal(self.mmatrix[2]),
        )
        self.y_vector = (
            dc.Decimal(self.mmatrix[4]),
            dc.Decimal(self.mmatrix[5]),
            dc.Decimal(self.mmatrix[6]),
        )
        self.z_vector = (
            dc.Decimal(self.mmatrix[8]),
            dc.Decimal(self.mmatrix[9]),
            dc.Decimal(self.mmatrix[10]),
        )

        self.trans = (
            dc.Decimal(self.mmatrix[12]),
            dc.Decimal(self.mmatrix[13]),
            dc.Decimal(self.mmatrix[14]),
        )

    def apply(self, node: str):
        """Applies the mmatrix attribute to any nodes given by argument.

        Args:
            node (str): Unique name of a node in scene.

        Raises:
            ValueError: If the node doesn't exist or isn't unique.
            TypeError: If the node isn't a transform or joint.
        """
        if cmds.objExists(node) == False:
            raise ValueError(f"{node} doesn't name a unique node found in the scene.")
        if cmds.nodeType(node) not in ["transform", "joint"]:
            raise TypeError(
                f"{node} is not joint or transform.  Can't apply a MMatrix."
            )
        # Create an MFnTransform function set for the transform node
        selection_list = om2.MGlobal.getSelectionListByName(node)
        dag_path = selection_list.getDagPath(0)
        transform_fn = om2.MFnTransform(dag_path)

        # Set the translation component of the transformation matrix
        # transform_fn.setTranslation(self.precise_trans) WHAT IS THE OTHER ARG FOR THIS?
        # Now how do I get the rotation?

    @property
    def precise_trans(self) -> tuple:
        return (
            dc.Decimal(self.mmatrix[12]),
            dc.Decimal(self.mmatrix[13]),
            dc.Decimal(self.mmatrix[14]),
        )

    @property
    def trans(self) -> tuple:
        return (self.mmatrix[12], self.mmatrix[13], self.mmatrix[14])

    @trans.setter
    def trans(self, value: iter):
        """Sets the fourth row values to reflect the given iterable.
        Args:
            value (iter): Tuple or list with three elements.

        Raises:
            TypeError: If anything within the iterable isn't the right type.
            ValueError: If the iterable contains more or less than 3 elements.
        """

        for val in value:
            if isinstance(val, (float, int, dc.Decimal)) == False:
                raise TypeError(f"{val} is not a float or int.")

        if len(value) != 3:
            raise ValueError(f"{value} doesn't contain exactly three values.")

        self.mmatrix[12] = value[0]
        self.mmatrix[13] = value[1]
        self.mmatrix[14] = value[2]

    @property
    def x_vector(self) -> tuple:
        return (self.mmatrix[0], self.mmatrix[1], self.mmatrix[2])

    @x_vector.setter
    def x_vector(self, value: iter):
        for val in value:
            if isinstance(val, (float, int, dc.Decimal)) == False:
                raise TypeError(f"{val} is not a float or int.")

        if len(value) != 3:
            raise ValueError(f"{value} doesn't contain exactly three values.")

        self.mmatrix[0] = value[0]
        self.mmatrix[1] = value[1]
        self.mmatrix[2] = value[2]

    @property
    def y_vector(self) -> tuple:
        return (self.mmatrix[4], self.mmatrix[5], self.mmatrix[6])

    @y_vector.setter
    def y_vector(self, value: iter):
        for val in value:
            if isinstance(val, (float, int, dc.Decimal)) == False:
                raise TypeError(f"{val} is not a float or int.")

        if len(value) != 3:
            raise ValueError(f"{value} doesn't contain exactly three values.")

        self.mmatrix[4] = value[0]
        self.mmatrix[5] = value[1]
        self.mmatrix[6] = value[2]

    @property
    def z_vector(self) -> tuple:
        return (self.mmatrix[8], self.mmatrix[9], self.mmatrix[10])

    @z_vector.setter
    def z_vector(self, value: iter):
        for val in value:
            if isinstance(val, (float, int, dc.Decimal)) == False:
                raise TypeError(f"{val} is not a float or int.")

        if len(value) != 3:
            raise ValueError(f"{value} doesn't contain exactly three values.")

        self.mmatrix[8] = value[0]
        self.mmatrix[9] = value[1]
        self.mmatrix[10] = value[2]

    def aim(
        self,
        subject: str,
        primary_target: str,
        secondary_target: str,
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

    def __getitem__(self, i):
        return self.mmatrix[i]

    def __setitem__(self, i, value):
        self.mmatrix[i] = value
