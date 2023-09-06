"""
colours.py
Created: Thursday, 31st August 2023 10:07:42 am
Matthew Riche
Last Modified: Thursday, 31st August 2023 10:07:47 am
Modified By: Matthew Riche
"""

import maya.cmds as cmds

colour_enum = {
    "grey": 0,
    "black": 1,
    "dark_grey": 2,
    "light_grey": 3,
    "dark_red": 4,
    "navy": 5,
    "blue": 6,
    "dark_green": 7,
    "dark_purple": 8,
    "purple": 9,
    "brown": 10,
    "dark_brown": 11,
    "dark_orange": 12,
    "red": 13,
    "bright_green": 14,
    "pale_blue": 15,
    "white": 16,
    "yellow": 17,
    "cyan": 18,
    "select_green": 19,
    "pink": 20,
    "pale_orange": 21,
    "pale_yellow": 22,
    "paleGreen": 23,
    "orange": 24,
    "dark_yellow": 25,
    "ugly_green": 26,
    "blue_green": 27,
    "dark_cyan": 28,
    "dark_blue": 29,
    "pale_purple": 30,
    "violet": 31,
}


def change_colour(node: str, colour="red", findShape=True):
    """Changes the colour override of a nodes in the scene.

    Args:
        nodes (str): _description_
        colour (str, optional): _description_. Defaults to "red".
        findShape (bool, optional): _description_. Defaults to True.

    Raises:
        NameError: If one object specified by nodes doesn't exist or isn't unique.
        TypeError: If the nodes has no shapes or is itself a shape.
    """

    if cmds.objExists(node) == False:
        raise NameError(f"'{node}' doesn't appear to exist in the scene.")

    if findShape:
        shapelist = cmds.listRelatives(node, shapes=True)
    else:
        shapelist = [node]

    if shapelist is not None:
        for shape in shapelist:
            cmds.setAttr(shape + ".overrideEnabled", True)
            cmds.setAttr(shape + ".overrideColor", colour_enum[colour])
    else:
        raise TypeError(f"'{node}' has no shape nodes, or itself is a shape nodes.")

    return
