import numpy as np


# Different camera views
cam = np.array([0, 0, -20])  # front
# cam = np.array([-20, 0, -20]) # side
# cam = np.array([25, 35, -20]) #top
# cam = np.array([30, -15, -30])  # slightly bottom

# Shuttle camera angles
#cam = np.array([30, -15, 150])
#cam = np.array([30, 50, 150])
# cam = np.array([0, 0, 200])


# Defining pRef, varies depending on objects
# pRef = np.array([-10, 0, 0])
# pRef = np.array([10, 15, 20]) #house from top
house_pRef = np.array([10, 0, 20])  # house from bottom
pRef = np.array([0, 0, 0])  # cow, bench
#pRef = np.array([0, 0, 0])


# Cow Camaro
pRef = np.array([10, 0, 20])
cam = np.array([-20, 0, -20])  # back

