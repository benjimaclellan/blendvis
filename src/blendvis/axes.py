import bpy
import copy
from math import radians
import pathlib
import time
from blendvis.primitives import FontPrimitive, LinePrimitive, CubePrimitive, CameraPrimitive

from blendvis import SAVE_PATH, DEFAULTS


class Axes:
    mat_axes  = "Black"
    mat_boxes = "Boxes"
    mat_font  = "Black"

    def __init__(self, verbose=False):
        self.X = None
        self.Y = None
        self.Z = None
        self.kwargs = {}
        self.verbose = verbose

        self.camera = None
        self.camera_aim = None

        self.xlim = [0, 1]
        self.ylim = [0, 1]
        self.title = ""
        self.yticklabels = [0, 1]
        self.xticklabels = [0, 1]


    # uses setattr to mimic the ax.set(xlim=[], ylim=[], title=[]) etc of matplotlib
    def set(self, **kwargs):
        for (key, val) in kwargs.items():
            setattr(self, key, val)

    def save(self):
        filename = SAVE_PATH
        bpy.context.scene.render.filepath = str(filename.absolute())
        bpy.ops.render.render(write_still=True)
        return

    def show(self):
        self.add_camera()


    def barplot(self, X, Y, Z, bevel=True, wireframe=False, mat=DEFAULTS['mat_bars']):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.kwargs['bevel'] = bevel
        self.kwargs['wireframe'] = wireframe

        for (x, y, z) in zip(self.X.flatten(), self.Y.flatten(), self.Z.flatten()):
            CubePrimitive(p=(x, y, 0), height=z, xy_scale=0.9, mat=mat).add_to_scene()
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            if self.kwargs['wireframe']:
                if self.verbose: print('adding a wireframe')
                bpy.ops.object.modifier_add(type='WIREFRAME')
            if self.kwargs['bevel']:
                if self.verbose: print('adding a bevel')
                bpy.ops.object.modifier_add(type='BEVEL')
                bpy.context.object.modifiers["Bevel"].width = 0.03
                bpy.context.object.modifiers["Bevel"].segments = 30


    def add_axes(self, xlim=(0, 1), ylim=(0, 1), mat=DEFAULTS['mat_axes']):
        LinePrimitive(p1=(xlim[0], ylim[0], 0), p2=(xlim[1], ylim[0], 0), plane='xy', thickness=0.2, mat=mat).add_to_scene()
        LinePrimitive(p1=(xlim[0], ylim[0], 0), p2=(xlim[0], ylim[1], 0), plane='xy', thickness=0.2, mat=mat).add_to_scene()
        return


    def add_tick_labels(self, x=[0, 1], xtick_labels=None, y=[0, 1], ytick_labels=None):
        XTICKBASE, YTICKBASE = 2 * [-0.8]
        if xtick_labels is None:
            xtick_labels = copy.copy(x)
        if ytick_labels is None:
            ytick_labels = copy.copy(y)

        for xi, xtick in zip(x, xtick_labels):
            FontPrimitive(text=str(xtick), p=(xi, XTICKBASE, 0)).add_to_scene()
        for yi, ytick in zip(y, ytick_labels):
            FontPrimitive(text=str(ytick), p=(YTICKBASE, yi, 0)).add_to_scene()
        return None

    def add_camera(self):
        CameraPrimitive(loc=(4, 4, 0), camera_aim_loc=(4, 4, 0)).add_to_scene()


