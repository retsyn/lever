'''
framework.py
Created: Wednesday, 13th September 2023 2:41:12 pm
Matthew Riche
Last Modified: Wednesday, 13th September 2023 2:41:17 pm
Modified By: Matthew Riche
'''

sides = {}
from enum import Enum

class Side(Enum):
    LEFT = 0
    CENTRE = 1
    RIGHT = 2



class RigFrame:
    def __init__(self):
        self.placer_queue = []
        self.built_placers = []
        self.side = Side.CENTRE

        self.build_commands = None
        self.post_build_commands = None

    def build_frame(self):
        pass
    
        