# knot-research

### Requirements:

[numpy](www.numpy.org)

[PyOpenGL](http://pyopengl.sourceforge.net/)

### Installation:

1. Install numpy
```pip install numpy```
2. Install PyOpenGL
```pip install PyOpenGL PyOpenGL_accelerate```

### Introduction

**Goal:** Given multiple replicas of a single module, find the best way
to fit them together to form a predefined type of mathematical knot.


**Azimuth Approach:**
Parameterize the space by "azimuth" or radial angles (the amount of twisting of each module along its center axis) of each individual module.

**Point Approach:**
Think only in terms of the center axes of each module. Parameterize the space by the points at the ends of each of these axes. Optimize to make the distances between these points as uniform as possible and the angles as close to the desired 30 degrees. Must account for z separation between knot branches so modules do not intersect.

**Template**
Contains template files I made for students to use when starting a project like this. Boiler plate code for defining geometry, building that geometry with PyOpenGL, and a crystal ball type interface for interacting with the OpenGL window.


