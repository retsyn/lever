"""
placer.py
Created: Friday, 30th June 2023 10:49:30 am
Matthew Riche
Last Modified: Friday, 30th June 2023 10:49:33 am
Modified By: Matthew Riche
"""

from . import build
from . import colours as cl
import maya.cmds as cmds


class Placer(build.BuildObject):
    def __init__(self, size, name, colour="yellow"):
        super().__init__(self)
        # Nurbs sphere placer is created and moved to the coords passed.
        new_placer = cmds.sphere(polygon=0, radius=size, name=name)[0]
        cmds.move(new_placer, self.trans)

        # Disconnect the initial Shader

        # Set up colour override
        cl.change_colour(new_placer, colour)

        return new_placer
