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

from . import vectors
from maya.api.OpenMaya import MVector

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
        self.oriet = (0.0, 0.0, 0.0)

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


class BuildObject:
    def __init__(self, position: MVector, name: str):
        self.trans = "UNSET"
        self.shape = "UNSET"
        self.type = "UNKNOWN"

        self.build(position=position)

        self.brand()

    def build(self, position):
        cmds.warning(
            "A BuildObject with no subclass got built.  Making a dud Octahedron"
        )
        self.trans = make_dud(position=position)

    def brand(self):
        """'brands' the transform node with the extra attributes that identify this as part of lvl.
        """

        cmds.addAttr(self.trans, longName="leverBuildObject", dt="string")
        # TODO Add this object to a "build_objects" layer.


def make_dud(position: MVector) -> str:
    """Makes a dud object as debug behaviour, if a BuildObject with no subclass runs or other
    'shouldn't happen' behaviours engage.

    Args:
        position (MVector): Vector position in absolute world space.
        name (str): A name given to this object.

    Returns:
        str: transform name.
    """

    if type(position) is not MVector:
        position = vectors.sanitize(position)

    new_solid_trans = cmds.polyPlatonicSolid(st=2, name="Dud")[0]
    cmds.xform(new_solid_trans, t=position, ws=True, a=True)

    return new_solid_trans
