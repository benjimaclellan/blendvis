import bpy
import pathlib
import importlib.resources
import json

from blendvis.materials import FlatRBG, GreasePencil
# from blendvis.figures import figure
# from blendvis.axes import Axes


with importlib.resources.open_text("blendvis", "rcParams.json") as file:
    rcParams = json.load(file)


# remove everything to start
def clear_collections():
    for coll in bpy.data.collections:
        for ob in coll.objects:
            coll.objects.unlink(ob)
        bpy.data.collections.remove(coll, do_unlink=True)


def clear_objects():
    for ob in bpy.data.objects:
        bpy.data.objects.remove(ob, do_unlink=True)


def clear_materials():
    for mat in bpy.data.materials:
       bpy.data.materials.remove(mat)


def clear_scenes():
    for scene in bpy.data.scenes:
        bpy.data.scenes.remove(scene)


def clear_worlds():
    for world in bpy.data.worlds:
        bpy.data.worlds.remove(world)



# #%%
# import numpy as np
#
#
# def auto_tick(tmin, tmax, nticks=6):
#     # finds a nice division of ticks lines based on upper and lower boundaries
#     # https://stackoverflow.com/questions/326679/choosing-an-attractive-linear-scale-for-a-graphs-y-axis
#     range_ = tmax - tmin
#
#     unrounded_tickrange = range_ / (nticks)
#     x = np.ceil(np.log10(unrounded_tickrange))
#     pow10x = np.power(10, x)
#     rounded_tickrange = np.ceil(unrounded_tickrange / pow10x) * pow10x
#
#     tmin_new = rounded_tickrange * np.floor(tmin / rounded_tickrange)
#     tmax_new = tmin_new + rounded_tickrange * (nticks - 1)
#
#     ticks = [tmin_new + i * rounded_tickrange for i in range(nticks)]
#     return (tmin_new, tmax_new), ticks
#
# out = auto_tick(-30, -4.6, nticks=8)
# print(out)
DEFAULTS = {
    'mat_axes': FlatRBG(name="axes", rgba=3 * [0.1] + [1]).add_to_scene(),
    'mat_bars': FlatRBG(name="boxes", rgba=(1, 1, 1, 1)).add_to_scene(),
    'mat_font': FlatRBG(name="fonts", rgba=(0, 0, 0, 1)).add_to_scene(),
    'black': FlatRBG(name="black", rgba=(0, 0, 0, 1)).add_to_scene(),
    'red': FlatRBG(name="red", rgba=(1, 0, 0, 1)).add_to_scene(),
    'blue': FlatRBG(name="blue", rgba=(0, 0, 1, 1)).add_to_scene(),
    'green': FlatRBG(name="green", rgba=(0, 1, 0, 1)).add_to_scene(),
}
SAVE_PATH = pathlib.Path(r"C:\Users\benjamin\OneDrive - University of Waterloo\Documents\IQC - Projects\Code\blendvis\examples\renders\3d-barplot.png")
MAIN_FONT = None

DEFAULT_FONT = DEFAULTS[rcParams['font_color']]
DEFAULT_GP = GreasePencil(name=rcParams['axes_color']).add_to_scene()


