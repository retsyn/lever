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
        self.size = size
        self.type = "Placer"
        super().__init__(position, name)
        
    def build(self):
        """Create a nurbs sphere with no shader.
        """  

        dprint("Building a placer...")
        
        # Nurbs sphere placer is created and moved to the coords passed.
        self.trans = cmds.sphere(polygon=0, radius=self.size, n=self.name)[0]
        self.shape = cmds.listRelatives(self.trans, s=True)[0]
        dprint(f"trans node is {self.trans}, shape ndoe is {self.shape}")
        # Disconnect the initial Shader
        shaders.remove_shader(self.shape)
        # Set up colour override
        cl.change_colour(self.trans, self.colour)
        
        dprint(f"Placer {self.trans} created.")


