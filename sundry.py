'''
sundry.py
Created: Sunday, 1st September 2024 3:39:27 pm
Matthew Riche
Last Modified: Sunday, 1st September 2024 3:39:34 pm
Modified By: Matthew Riche
'''

import random

def random_vector(rot=False):
    """Generate randomized coordinates in space for robust testing.

    Returns:
        tuple: Random euler vector
    """

    if rot == False:
        lower_bound = -1000000.0
        upper_bound = 1000000.0
    else:
        lower_bound = -360.0
        upper_bound = 360.0

    x = random.uniform(lower_bound, upper_bound)
    y = random.uniform(lower_bound, upper_bound)
    z = random.uniform(lower_bound, upper_bound)

    return (x, y, z)