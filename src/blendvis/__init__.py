import pathlib
import bpy

import blendvis.materials

DEFAULTS = {'mat_axes': blendvis.materials.FlatRBG(name="axes", rgba=3 * [0.1] + [1]).add_to_scene(),
            'mat_bars': blendvis.materials.FlatRBG(name="boxes", rgba=(1, 1, 1, 1)).add_to_scene(),
            'mat_font': blendvis.materials.FlatRBG(name="fonts", rgba=(0, 0, 0, 1)).add_to_scene()}
SAVE_PATH = pathlib.Path(r"C:\Users\benjamin\OneDrive - University of Waterloo\Documents\IQC - Projects\Code\blendvis\examples\renders\3d-barplot.png")


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


# add in the collections that sort the objects in the scene
def init_collections():
    for coll in ['MAIN', 'FONTS', 'LINES', 'MESHES', 'CAMERA']:
        c = bpy.data.collections.new(coll)
        bpy.context.scene.collection.children.link(c)

