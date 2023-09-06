'''
shaders.py
Created: Wednesday, 6th September 2023 9:54:22 am
Matthew Riche
Last Modified: Wednesday, 6th September 2023 9:54:29 am
Modified By: Matthew Riche
'''

import maya.cmds as cmds


def remove_shader(shape_node:str):
    """Removes the shader from an object so that it's only coloured by it's override.

    Args:
        shape_node (str): Name of the node to un-shade.

    Raises:
        NameError: If a non-existent node is specified.
        TypeError: If a transform node is given.
    """    

    if(cmds.objExists(shape_node) == False):
        raise NameError(f"{shape_node} doesn't exist or isn't unique.")

    if(cmds.nodeType(shape_node) == 'transform'):
        raise TypeError(f"{shape_node} was a transform node, this should only be run on shapes.")
    
    cmds.disconnectAttr(f'{shape_node}.instObjGroups', 'initialShadingGroup.dagSetMembers', na=True)