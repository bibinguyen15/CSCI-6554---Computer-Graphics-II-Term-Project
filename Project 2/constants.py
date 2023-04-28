import numpy as np


'''
File to hold all different camera and pRef values
'''

# Different camera views
#cam = np.array([0, 0, -20])  # front
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
#house_pRef = np.array([10, 0, 20])
#pRef = np.array([0, 0, 0])  # cow, bench
#pRef = np.array([0, 0, 0])


## From top
#house_pRef = np.array([15, 15, 15])
#house_cam = np.array([20, 25, -10])

#benchbig_cam = np.array([5, 10, -15])


## Cow Camaro from back
#pRef = np.array([10, 0, 20])
#cam = np.array([-20, 0, -20])  # back

##Cow Camro from top
#cow_pRef = np.array([0, 0, 20])
#camaro_pRef = np.array([0, 0, 20])
#cam = np.array([10, 15, -25])


# Bench and car from front
cam = np.array([0, 0, -5])  # front
bench_pRef = np.array([0, 0, 0])
car_pRef = np.array([0, 0, 0])
