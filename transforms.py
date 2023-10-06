"""
transforms.py
Created: Friday, 6th October 2023 12:36:59 pm
Matthew Riche
Last Modified: Friday, 6th October 2023 12:37:03 pm
Modified By: Matthew Riche
"""

from .lvnode import LvNode
from typing import Union
import maya.cmds as cmds

def aim_at(
    node: Union[LvNode, str],
    target: Union[LvNode, str],
    up_object: Union[LvNode, str],
    primary_axis="y",
    secondary_axis="x",
):
    """Aims an object at a target, and secondary axis at the up-object.  I very badly wanted to use
    pure calculation without creating temporary nodes, but after many struggles with the math, I 
    found that a temporary node, if I delete right away, isn't unreasonable, and every TD is
    probably doing it this way.

    Args:
        node (Union[LvNode, str]): The node to re-orient.
        target (Union[LvNode, str]): The node to aim-at.
        up_object (Union[LvNode, str]): The node to align secondary axis.
        primary_axis (str, optional): Which axis to aim. Defaults to "y".
        secondary_axis (str, optional): Which axis is secondary. Defaults to "x".

    Raises:
        ValueError: If the node isn't found in the scene.
        TypeError: If the node isn't transformable.
        ValueError: If an LvNode is used and the object it points to is gone.
        TypeError: If the object arguments aren't str or LvNode.
        ValueError: If the primary axis isn't x, y, or z.
        ValueError: If the primary axis is the same as the secondary axis.
        AssertionError: If the rotation channels are locked or connected.
    """    
    # Clean up args and throw errors for bad values or types.
    for arg in [node, target, up_object]:
        if isinstance(arg, str):
            if cmds.objExists(arg) == False:
                raise ValueError(
                    f"No node named {arg} is found in the scene, or isn't unique."
                )
            elif cmds.objectType(arg) not in ["transform", "joint"]:
                raise TypeError(f"Can't orient a node with no transform data.")
        elif isinstance(arg, LvNode):
            if cmds.objExists(arg.name) == False:
                raise ValueError(
                    f"LvNode {arg} has a name ({arg.name}) pointing to a not found",
                    "or not unique object.",
                )
        else:
            raise TypeError(f"{arg} must be a str or LvNode, not {type(arg)}")
        
    # Pluck the name out of LvNodes.
    if(isinstance(node, LvNode)):
        node = node.name
    if(isinstance(target, LvNode)):
        target = target.name
    if(isinstance(up_object, LvNode)):
        up_object = up_object.name

    # Prevent nonsense values for primary and secondary axis.
    for arg in [primary_axis, secondary_axis]:
        if (arg) not in ["x", "y", "z"]:
            raise ValueError("Chosen axis must be x, y, or z.")
        if primary_axis == secondary_axis:
            raise ValueError("Axis can't be the same.")

    # Throw an error if this rotation is already connected or locked.
    channel_checks = [".rx", ".ry", ".rz"]
    for channel in channel_checks:
        if cmds.getAttr(f"{node}{channel}", se=True) == False:
            raise AssertionError(
                f"{node}{channel} is locked or connected, can't orient it."
            )

    def _letter_to_vec(letter):
        if letter == "x":
            return [1.0, 0.0, 0.0]
        elif letter == "y":
            return [0.0, 1.0, 0.0]
        elif letter == "z":
            return [0.0, 0.0, 1.0]
        else:
            raise ValueError (f"Bad axis letter: {letter}")

    aim_vec = _letter_to_vec(primary_axis)
    up_vec = _letter_to_vec(secondary_axis)
    
    # Let the dag orient this after the application of the temp aim constraint, then clean it.
    print(f"aim vec is {aim_vec} and up_vec")
    temp_constraint = cmds.aimConstraint(
        target, node, wut="object", wuo=up_object, aim=aim_vec, u=up_vec
    )
    cmds.delete(temp_constraint)
