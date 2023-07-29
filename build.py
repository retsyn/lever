'''
build.py
Created: Friday, 30th June 2023 10:54:15 am
Matthew Riche
Last Modified: Friday, 30th June 2023 10:54:22 am
Modified By: Matthew Riche

This module is for building generic objects in the scene with a common super-class.
Things like 'placers' are found in other modules, that inherit some of these classes and use 
some of these defs.
'''

from . import vectors
from maya.api.OpenMaya import MVector

import maya.cmds as cmds

class BuildObject:
    def __init__(self, position: MVector, name: str):
        self.trans = "UNSET"
        self.shape = "UNSET"
        self.type = "UNKNOWN"

        self.build(position=position)

        self.brand()

    def build(self, position):
        cmds.warning("A BuildObject with no subclass got built.  Making a dud Octahedron")
        self.trans = make_dud(position=position)

        
        
    def _brand(self):
        """'brands' the transform node with the extra attributes that identify this as part of lvl.
        """        

        cmds.addAttr(self.trans, longName='leverBuildObject', dt='string')
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

    if(type(position) is not MVector):
        position = vectors.sanitize(position)
    
    new_solid_trans = cmds.polyPlatonicSolid(st=2, name="Dud")[0]
    cmds.xform(new_solid_trans, t=position, ws=True, a=True)

    return new_solid_trans
    