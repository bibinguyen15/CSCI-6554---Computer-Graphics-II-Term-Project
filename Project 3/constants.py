import numpy as np


'''
File to hold all constant values
'''

# Different camera views
#cam = np.array([0, 0, -20])  # front
# cam = np.array([-20, 0, -20]) # side
# cam = np.array([25, 35, -20]) #top
# cam = np.array([30, -15, -30])  # slightly bottom

# Shuttle camera angles
#cam = np.array([30, -15, 150])
#cam = np.array([30, 50, 150])
#cam = np.array([0, 0, 200])


# Defining pRef, varies depending on objects
pRef = np.array([-10, 0, 0])
# pRef = np.array([10, 15, 20]) #house from top
#house_pRef = np.array([10, 0, 20])
#pRef = np.array([0, 0, 0])  # cow, bench
#pRef = np.array([0, 0, 0])


## From top
house_pRef = np.array([15, 15, 15])
house_cam = np.array([20, 25, -10])

#benchbig_cam = np.array([5, 10, -15])


## Cow Camaro from back
camaro_pRef = np.array([10, 0, 20])
cow_pRef = np.array([10, 0, 20])
#cam = np.array([-20, 0, -20])  # back

##Cow Camro from top
#cow_pRef = np.array([0, 0, 20])
#camaro_pRef = np.array([-10, -9, 20])
#cam = np.array([10, 15, -25])


# Bench and car from front
cam = np.array([0, 0, -5])  # front
bench_pRef = np.array([0, 0, 0])
car_pRef = np.array([0, 0, 0])
betterBall_pRef = np.zeros(3)

#Modes: -1 for constant, 0 for Gouraud, 1 for Phong Shading
mode = 0

#Illumination constants
#Constant Shading
ka = 0.3
kd = 0.5
ks = 0.8
L = np.array([25, 50, -500])
#L = np.array([500, -10, -65])
#L = np.array([500, -100, -300])
V = np.array([0, 0, -5])
sourceColor = np.array([1, 1, 1])

###Gouraud Shading
ka = 0.1
kd = 0.3
ks = 0.8
#L = np.array([5, -5, -25])
V = np.array([0, 0, 0])
sourceColor = np.array([1, 1, 1])


##Phong Shading
#ka = 0.1
#kd = 0.2
#ks = 0.9
#L = np.array([25, 50, -500])
#V = np.array([0, 0, 0])
#sourceColor = np.array([0.5, 0.5, 0.5])

#Shuttle
#ka = 0.3
#kd = 0.1
#ks = 0.8
##L = np.array([-135, -30, 30])
##L = np.array([80, -50, 20])
#L = np.array([380, -70, 20]) #cow
#V = np.array([70, -50, 0])
#sourceColor = np.array([0.3, 0.3, 0.3])
