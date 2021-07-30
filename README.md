# blendvis: Blender Visualization Tool for 3D Scientific Plotting 


## Quick Start
`blendvis` is designed with two main principles; 
to closely follow the syntax of the `matplotlib.pyplot` library for ease-of-use, and to
use the powerful 3D modelling, animation, and rendering capabilities of [Blender](https://www.blender.org/).

## Examples
To show how the `blendvis` library can be used, we will make a 3D barplot figure that simulates some 
experimental data and theoretical data, plotting both together.
```
import blendvis

# Simulate some experimental and theoretical data
M, N = 10, 10
x, y = np.arange(1, M), np.arange(1, N)
X, Y = np.meshgrid(x, y)
Zth = np.random.randint(-1, 2, [M, N])
Zex = Zth * np.random.uniform(0.8, 1, [M, N])

# Create a Blender scene with the data
ax = blendvis.axes.Axes(verbose=False)
ax.barplot(X, Y, Zex, bevel=True, wireframe=False, mat='Boxes')
ax.barplot(X, Y, Zth, bevel=False, wireframe=True, mat='Black')
ax.show()

ax.add_axes(xlim=[0, 10], ylim=[0, 10])
ax.add_tick_labels(x=x, y=y)

# Add a camera and set up render settings, render an image and save
ax.show()
ax.save()
```
which generates the figure,
![Example 3d-barplot](examples/renders/3d-barplot.png)

## Installing
Currently, `blendvis` must be run via an instance of Blender. 
First [download](https://www.blender.org/download/) and install Blender (the 2.93 LTS version is recommended).
Copy-paste one of the example .blend files and start from there.

## Limitations
Stay tuned - improvements to come! 