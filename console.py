'''
console.py
Created: Wednesday, 6th September 2023 11:34:51 am
Matthew Riche
Last Modified: Wednesday, 6th September 2023 11:34:57 am
Modified By: Matthew Riche
'''

from . import settings

def dprint(text:str):
    """Just a print, but only with a debug flag.

    Args:
        text (str): Message to print to console
    """    
    if(settings.debug):
        print(text)