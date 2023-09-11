"""
placer.py
Created: Friday, 30th June 2023 10:49:30 am
Matthew Riche
Last Modified: Friday, 30th June 2023 10:49:33 am
Modified By: Matthew Riche
"""

from . import build
from . import colours as cl
from . import shaders
from .console import dprint
import maya.cmds as cmds


class Placer(build.BuildObject):
    def __init__(self, position: tuple, size: float, name: str, colour="yellow"):
        self.colour = colour
        self._size = size
        self.type = "Placer"
        super().__init__(position, name)
        
    def build(self):
        """Create a nurbs sphere with no shader.
        """  

        dprint("Building a placer...")
        
        # Nurbs sphere placer is created and moved to the coords passed.
        self.trans = cmds.sphere(polygon=0, radius=self._size, n=self.name)[0]
        self.shape = cmds.listRelatives(self.trans, s=True)[0]
        dprint(f"trans node is {self.trans}, shape ndoe is {self.shape}")
        # Disconnect the initial Shader
        shaders.remove_shader(self.shape)
        # Set up colour override
        cl.change_colour(self.trans, self.colour)
        
        dprint(f"Placer {self.trans} created.")

    @property
    def size(self):
        # This should derive from the scale of the trans node.
        return self._size
    
    @size.setter
    def size(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError(f"Size must be a float or int, not {type(value)}.")
        else:
            self._size = value

    @property
    def translate(self):
        return cmds.xform(self.trans, q=True, t=True, ws=True, a=True)

    @translate.setter
    def translate(self, value):
        if not isinstance(value, (list, tuple)):
            raise TypeError("Translate values must be lists or tuples.")
        if len(value) != 3:
            raise ValueError("Translate value requires three elements.")

        cmds.xform(self.trans, q=False, t=value, ws=True, a=True)

            


