"""
lvnode.py
Created: Thursday, 7th September 2023 4:26:24 pm
Matthew Riche
Last Modified: Thursday, 7th September 2023 4:26:31 pm
Modified By: Matthew Riche
"""

import maya.cmds as cmds
import maya.api.OpenMaya as om2
import decimal as dc

from . import console as cnsl


dc.getcontext().prec = 16


class LvNode:
    def __init__(self, node_name: str):
        """A re-implementation of some of the favorite aspects of PyNodes.

        Args:
            node_name (str): in-scene name of node.

        Raises:
            NameError:
        """

        if cmds.objExists(node_name) == False:
            raise NameError(f"{node_name} not found in scene or is not unique.")

        self.uuid = cmds.ls(node_name, uuid=True)[0]
        self.name = node_name
        self.oldname = node_name # Extra storage of "last known name" to prevent attr recursion 

    def valid(self) -> bool:
        return(cmds.objExists(self.name))

    def delete_node(self):
        """Deletes the node represented in Maya.  
        """
        if(self.valid()):
            cmds.delete(self.name)
        else:
            raise ValueError(f"{self.name} doesn't exist in the scene.")

    @property
    def name(self) -> str:
        """Get the current flattened name based on UUID.

        Returns:
            str: In-Scene node name.
        """
        return cmds.ls(self.uuid, uuid=True, long=False)[0]

    @name.setter
    def name(self, value: str):
        """Identifies the node based on UUID, and renames it to given value.

        Args:
            value (str): New name for the node.
        """
        if(self.valid() == False):
            raise ValueError("{self.name} is missing from the scene.")
        current_name = cmds.ls(self.uuid, uuid=True, long=True)
        self.oldname = current_name
        cmds.rename(current_name, value)

    @property
    def long_name(self) -> str:
        """A Non-flattened name, safer for internal operations.

        Returns:
            str: The full pathed name.
        """
        if(self.valid() == False):
            raise ValueError("{self.name} is missing from the scene.")
        return cmds.ls(self.uuid, uuid=True, long=True)[0]

    @property
    def translate(self):
        if(self.valid() == False):
            raise ValueError("{self.name} is missing from the scene.")

        return cmds.xform(self.long_name, q=True, t=True, ws=True, a=True)

    @translate.setter
    def translate(self, value):
        if(self.valid() == False):
            raise ValueError("{self.name} is missing from the scene.")

        if len(value) != 3:
            raise ValueError("Translate value requires three elements.")
        for v in value:
            if(isinstance(v, (float, int, dc.Decimal)) == False):
                raise TypeError(f"{v} is not float, int, or Decimal.")

        cmds.xform(self.long_name, q=False, t=value, ws=True, a=True)

    @property
    def local_translate(self):
        if(self.valid() == False):
            raise ValueError("{self.name} is missing from the scene.")

        return cmds.xform(self.long_name, q=True, t=True, ws=False, a=True)

    @property
    def rotate(self):
        if(self.valid() == False):
            raise ValueError("{self.name} is missing from the scene.")

        return cmds.xform(self.name, q=True, ro=True, ws=True, a=True)

    @rotate.setter
    def rotate(self, value):
        
        if(self.valid() == False):
            raise ValueError("{self.name} is missing from the scene.")
        
        if isinstance(value, (float, int)):
            raise TypeError("Rotate values must be lists or tuples.")
        if len(value) != 3:
            raise ValueError("Rotate value requires three elements.")

        cmds.xform(self.long_name, q=False, ro=value, ws=True, a=True)

    def __str__(self):
        return f"{self.name}'"
    
    def __del__(self):
        # When Python garbage collection happens, we should warn we don't have LvNodes anymore.
       
        cnsl.dprint(
            f"{self.oldname} still exists is losing it's LvNode connection. " 
            "(Normal if execution is ending)"
        )
        


