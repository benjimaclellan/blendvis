import pathlib
import bpy

DEFAULTS = {'mat_axes': "Black", 'mat_bars': "Boxes", 'mat_font': "Black"}
SAVE_PATH = pathlib.Path(r"C:\Users\benjamin\OneDrive - University of Waterloo\Documents\IQC - Projects\Code\blendvis\examples\renders\3d-barplot.png")


# remove everything to start
def clear():
    for coll in bpy.data.collections:
        for ob in coll.objects:
            coll.objects.unlink(ob)
        bpy.data.collections.remove(coll, do_unlink=True)

    for ob in bpy.data.objects:
        bpy.data.objects.remove(ob, do_unlink=True)


# add in the collections that sort the objects in the scene
def init():
    for coll in ['MAIN', 'FONTS', 'LINES', 'MESHES', 'CAMERA']:
        c = bpy.data.collections.new(coll)
        bpy.context.scene.collection.children.link(c)

clear()
init()
