import bpy
import pathlib
import importlib.resources
import json

from blendvis.materials import FlatRGB, GreasePencil
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


DEFAULTS = {
    'mat_axes': FlatRGB(name="axes", rgba=3 * [0.1] + [1]).add_to_scene(),
    'mat_bars': FlatRGB(name="boxes", rgba=(1, 1, 1, 1)).add_to_scene(),
    'mat_font': FlatRGB(name="fonts", rgba=(0, 0, 0, 1)).add_to_scene(),
    'black': FlatRGB(name="black", rgba=(0, 0, 0, 1)).add_to_scene(),
    'red': FlatRGB(name="red", rgba=(1, 0, 0, 1)).add_to_scene(),
    'blue': FlatRGB(name="blue", rgba=(0, 0, 1, 1)).add_to_scene(),
    'green': FlatRGB(name="green", rgba=(0, 1, 0, 1)).add_to_scene(),
}

print(bpy.path.abspath("//"))
SAVE_PATH = pathlib.Path(bpy.path.abspath("//")).joinpath('renders')
MAIN_FONT = None

DEFAULT_FONT = DEFAULTS[rcParams['font_color']]
DEFAULT_GP = GreasePencil(name=rcParams['axes_color']).add_to_scene()


