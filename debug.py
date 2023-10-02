"""
debug.py
Created: Monday, 2nd October 2023 4:45:39 pm
Matthew Riche
Last Modified: Monday, 2nd October 2023 4:45:46 pm
Modified By: Matthew Riche
"""


# Debugging for other parts of the suite, or any tools using them.  Visualizes vectors and matrices
# As nurbs in a scene to double check your math.

import maya.cmds as cmds
from maya.api.OpenMaya import MVector, MMatrix
from . import vectors


def show_vector(vector, start_point=vectors.LVector(0.0, 0.0, 0.0), n="debug_line_vector", colour=1):
    """Creates a 1-degree nurbsCurve in the scene that shows the magnitude and direction of a line
    Vector.

    Args:
        vector (iterable): iterable of length 3 like MVector, list, or tuple.
        start_point (iterable, optional): Initial transform of the line vector. Defaults to None.
        n (str, optional): In-scene name that will be used. Defaults to "debug_line_vector".

    Returns:
        str: name of the nurbsCurve's transform node created in the scene.
    """

    # There won't be any sanitization of the arg, since that's handled in the vectors module, and
    # this module is likely going to be debugging solely the work of that module.
    vector = vector + start_point
    vector_line = cmds.curve(d=1, p=[start_point, vector], name=n)

    recolour(vector_line, colour=colour)

    return vector_line


def show_matrix(matrix, name="debug_matrix"):
    """Using 1-degree nurbsCurves, 'draw' a visualization of a matrix in-scene.

    Args:
        matrix (2-dimensional iterable): The input matrix to draw.
        n (str, optional): In-scene names of drawn nodes. Defaults to "debug_matrix".
    """

    # MMatrix class doesn't have two dimensional iterables, but instead getElement;
    if type(matrix) is MMatrix:
        translate = (
            matrix.getElement(3, 0),
            matrix.getElement(3, 1),
            matrix.getElement(3, 2),
        )
        x_vec = (
            matrix.getElement(0, 0),
            matrix.getElement(0, 1),
            matrix.getElement(0, 2),
        )
        y_vec = (
            matrix.getElement(1, 0),
            matrix.getElement(1, 1),
            matrix.getElement(1, 2),
        )
        z_vec = (
            matrix.getElement(2, 0),
            matrix.getElement(2, 1),
            matrix.getElement(2, 2),
        )

    # We want to also handle 2D iterables;
    elif type(matrix) in [list, tuple]:
        translate = matrix[3][:3]
        x_vec = matrix[0][:3]
        y_vec = matrix[1][:3]
        z_vec = matrix[2][:3]
    else:
        raise ValueError("Provided matrix can't be parsed as a matrix.")

    x_nurbs = show_vector(
        x_vec + translate, start_point=translate, n=(name + "_x_axis")
    )
    y_nurbs = show_vector(
        y_vec + translate, start_point=translate, n=(name + "_y_axis")
    )
    z_nurbs = show_vector(
        z_vec + translate, start_point=translate, n=(name + "_z_axis")
    )

    recolour(x_nurbs, colour=13)
    recolour(y_nurbs, colour=14)
    recolour(z_nurbs, colour=15)


def recolour(node, colour=1):
    """Recolours the override of a node's shape.

    Args:
        node (str): Name of a node in-scene
        colour (int, optional): colour index for colour override. Defaults to 1.

    Raises:
        TypeError: If no shape node can be found beneath the target.
    """

    shape_node = cmds.listRelatives(node, s=True)[0]
    if shape_node is None:
        raise TypeError("{} has no shape, won't recolour it.".format(node))

    cmds.setAttr(shape_node + ".overrideEnabled", 1)
    cmds.setAttr(shape_node + ".overrideColor", colour)
    cmds.setAttr(shape_node + ".lineWidth", 2.0)
