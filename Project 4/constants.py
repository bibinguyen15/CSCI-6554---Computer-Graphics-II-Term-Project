import numpy as np

'''
File to hold all constant values
'''

# What shading mode to use
# -1 Constant, 0 Gouraud, 1 Phong
mode = -1

# Donut Constants
# #Transformation constants
# cam = np.array([0, 1, -3])
# pRef = np.zeros(3)
#
# #Illumination constants
# n = 100
# color = [0.9, 0.6, 0.8]
# ka = 0.4
# kd = 0.4
# ks = 0.9
# V = np.array([0, 0, 15])
# sourceLight = np.array([1, 1, 1])
# L = np.array([-15, 5, -50])

#Better Ball constants
#Transformation constants
cam = np.array([0, 0, -6])
pRef = np.zeros(3)

#Illumination constants
n = 350
color = [0.9, 0.6, 0.8]
ka = 0.4
kd = 0.4
ks = 0.9
V = np.array([0, 0, 15])
sourceLight = np.array([1, 1, 1])
L = np.array([10, 10, -250])

# # Cow constants
# #Transformation data
# cow_pRef = np.array([10, 0, 20])
# cow_cam = np.array([-20, 0, -20])
#
# #Illumination constants
# n = 500
# color = [0.4, 0.3, 0.3]
# ka = 0.4
# kd = 0.4
# ks = 0.95
# V = np.array([0, 0, 15])
# sourceLight = np.array([1, 1, 1])
# L = np.array([10, 23, -450])


# textureFile = "textures\\Star.jpg"
textureFile = "textures\\wrinkles.jpg"
