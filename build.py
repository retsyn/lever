"""
build.py
Created: Friday, 30th June 2023 10:54:15 am
Matthew Riche
Last Modified: Friday, 30th June 2023 10:54:22 am
Modified By: Matthew Riche

This module is for building generic objects in the scene with a common super-class.
Things like 'placers' are found in other modules, that inherit some of these classes and use 
some of these defs.
"""

from maya.api.OpenMaya import MVector
from .console import dprint

import maya.cmds as cmds

# TODO: Smart-naming module that pulls apart strings by token.


class BuildJoint:
    def __init__(
        self,
        reference_node=None,
        parent_joint=None,
        position=(0.0, 0.0, 0.0),
        orient=(0.0, 0.0, 0.0),
        name=None,
    ):
        self.position = (0.0, 0.0, 0.0)
        self.orient = (0.0, 0.0, 0.0)

        # If there is a reference node in the scene, let's learn from it.
        if reference_node is not None:
            if cmds.objExists(reference_node) == False:
                raise NameError(f"No joint in the scene named {reference_node}")
            elif cmds.objectType(reference_node) != "joint":
                raise TypeError(f"{reference_node} is not of type joint.")
            # Conditions met to learn from this node.
            self.position = cmds.xform(reference_node, q=True, ws=True, t=True)
            self.orient = cmds.getAttr(reference_node + ".jointOrient")
            self.parent_joint = cmds.listRelatives(reference_node, p=True)[0]
            self.name = (
                reference_node  # TODO A smart naming convention class is needed.
            )
        else:
            # If there's no in-scene reference joint, build via parameters.
            self.position = position
            if parent_joint is not None:
                self.parent_joint = parent_joint
            self.orient = orient


class PlanObject:
    def __init__(self, position: MVector, name="Generic Build Object"):
        """Generic build object that will inform other objects in Lever.

        Args:
            position (MVector): Position in space.
            name (str, optional): Name of the build-object. Defaults to "Generic Build Object".
        """
        dprint(f"Initializing a PlanObject named {name}")
        self.trans = "UNSET"
        self.shape = "UNSET"
        self.type = "UNKNOWN"
        self.position = position
        self.name = name  # Possible not needed because of UUIDs?
        self.uuid = ""
        

        self.build()

        self.place()

        self.brand()

    def build(self):
        """Turn this object into a functioning rig-piece."""
        cmds.warning(
            "A PlanObject with no subclass got built.  Making a dud Octahedron"
        )
        self.trans = make_dud(position=self.position)
        self.name = self.trans
        self.shape = cmds.listRelatives(self.trans, s=True)[0]

    def place(self):
        """Moves the transform to the desired position"""

        dprint(f"Moving {self.trans} to {self.position}.")
        cmds.xform(self.trans, t=self.position, ws=True, a=True)

    def brand(self):
        """'brands' the transform node with the extra attributes that identify this as part of lvl."""

        cmds.addAttr(self.trans, longName="leverBuildObject", dt="string")
        # TODO Add this object to a "build_objects" layer.

    @property
    def name(self):
        return cmds.ls(self.uuid, uuid=True, long=False)[0]

    @property
    def translation(self):
        """Uses the current worldspace position of the trans node as a property.

        Returns:
            list: Direct output of cmds.xform, in the form of [x, y, z]
        """
        return cmds.xform(self.trans, q=True, t=True, ws=True, a=True)

    @translation.setter
    def translation(self, value: iter):
        """Setter for translation, passes through to the actual node position in the scene.

        Args:
            value (iter): World space euler position.

        Raises:
            ValueError: If the position is not the right kind of iterable (too long, too short.)
        """
        if len(value) != 3:
            raise ValueError("Translation value must be (x, y, z)")
        else:
            cmds.xform(self.trans, t=value, ws=True, a=True)

    @property
    def rotation(self):
        """Encapsulation of the rotation channels.

        Returns:
            _type_: _description_
        """
        return cmds.xform(self.trans, q=True, ro=True, ws=True, a=True)

    @rotation.setter
    def rotation(self, value: iter):
        """Setter function encapsulation of the rotation channels.

        Args:
            value (iter): Any iterable with 3 elements, representing x,y,z

        Raises:
            ValueError: If the length of value is not 3.
        """
        if len(value) != 3:
            raise ValueError("Rotation value must be (x, y, z)")
        else:
            cmds.xform(self.trans, ro=value, ws=True, a=True)

    @classmethod
    def clean_all(self):
        """Cleans up all build-objects in the scene."""
        to_delete = [
            node
            for node in cmds.ls()
            if cmds.attributeQuery("leverBuildObject", node=node, exists=True)
        ]
        dprint(f"Cleaning {len(to_delete)} objects.")
        cmds.delete(to_delete)

    def __str__(self):
        return f"Lever Build object called {self.name}.  Type: {self.type}."


class RigStructure:
    def __init__(self):
        self.name
        self.type

        self.build_objects = []

    def build(self):
        cmds.error("A generic RigStructure tried to build!  Nothing will happen.")


def make_dud(position: MVector) -> str:
    """Makes a dud object as debug behaviour, if a PlanObject with no subclass runs or other
    'shouldn't happen' behaviours engage.

    Args:
        position (MVector): Vector position in absolute world space.
        name (str): A name given to this object.

    Returns:
        str: transform name.
    """

    new_solid_trans = cmds.polyPlatonicSolid(st=2, name="Dud")[0]
    cmds.xform(new_solid_trans, t=position, ws=True)


    return new_solid_trans
