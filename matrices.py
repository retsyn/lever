"""
matrices.py
Created: Sunday, 17th September 2023 7:55:08 pm
Matthew Riche
Last Modified: Sunday, 17th September 2023 7:55:11 pm
Modified By: Matthew Riche
"""

import maya.cmds as cmds
import maya.api.OpenMaya as om2
from . import vectors


def get_matrix(node: str):
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
        raise ValueError(f"{node} isn't a node found in the scene (Or is not unique).")
    elif cmds.objectType(node) not in ["joint", "transform"]:
        raise TypeError(f"{node} is not of type joint or transform.")

    # Get a dagpath in order toget a MFnTransform in order to return a MMatrix.
    selection_list = om2.MGlobal.getSelectionListByName(node)
    dag_path = selection_list.getDagPath(0)
    transform_fn = om2.MFnTransform(dag_path)

    return transform_fn.transformation().asMatrix()


def aim(
    node: str,
    primary_target: str,
    secondary_target: str,
    primary_axis='y',
    secondary_axis='x',
):
    for node_name in [node, primary_target, secondary_target]:
        if cmds.objExists(node_name) == False:
            raise ValueError(
                f"{node_name} doesn't exist in the scene or is not unique."
            )
        if cmds.objectType(node_name) not in ["transform", "joint"]:
            raise TypeError(f"{node} not of type joint or transform.")

    for axis_value in [primary_axis, secondary_axis]:
        if axis_value not in ["x", "y", "z"]:
            raise ValueError(
                f"primary and secondary axis must be 'x', 'y', or 'z', not {axis_value}."
            )

    subject_matrix = get_matrix(node)
