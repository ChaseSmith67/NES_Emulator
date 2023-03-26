# Author: Chase Smith
# GitHub username: ChaseSmith67
# Date: 3/26/23
# Description: Array of 8-bit integers that will serve as the Random
#               Access Memory for the system.


import numpy as np

# Number of Kilobytes of RAM, change this variable to adjust
KB = 2

ram = np.array([0] * (KB * 1024), dtype=np.uint8)

