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
        current_name = cmds.ls(self.uuid, uuid=True, long=True)
        cmds.rename(current_name, value)

    @property
    def long_name(self) -> str:
        """A Non-flattened name, safer for internal operations.

        Returns:
            str: The full pathed name.
        """

        return cmds.ls(self.uuid, uuid=True, long=True)[0]

    @property
    def translate(self):
        return cmds.xform(self.long_name, q=True, t=True, ws=True, a=True)

    @translate.setter
    def translate(self, value):
        if len(value) != 3:
            raise ValueError("Translate value requires three elements.")
        for v in value:
            if(isinstance(v, (float, int, dc.Decimal)) == False):
                raise TypeError(f"{v} is not float, int, or Decimal.")

        cmds.xform(self.long_name, q=False, t=value, ws=True, a=True)

    @property
    def local_translate(self):
        return cmds.xform(self.long_name, q=True, t=True, ws=False, a=True)

    @property
    def rotate(self):
        return cmds.xform(self.name, q=True, ro=True, ws=True, a=True)

    @rotate.setter
    def rotate(self, value):
        if isinstance(value, (float, int)):
            raise TypeError("Rotate values must be lists or tuples.")
        if len(value) != 3:
            raise ValueError("Rotate value requires three elements.")

        cmds.xform(self.long_name, q=False, ro=value, ws=True, a=True)

    def __str__(self):
        return f"{self.name}'"


