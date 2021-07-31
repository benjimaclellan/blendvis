import bpy
import copy
import numpy as np
from math import radians
import pathlib
import time
from blendvis.primitives import FontPrimitive, LinePrimitive, CubePrimitive, CameraPrimitive, SpherePrimitive
from blendvis.materials import FlatRBG, ColorGradient, Material

from blendvis import SAVE_PATH, DEFAULTS


def check(kwargs, key):
    if key in kwargs.keys():
        if kwargs[key]:
            return True
    return False


class Axes:
    # mat_axes  = "Black"
    # mat_boxes = "Boxes"
    # mat_font  = "Black"

    def __init__(self, verbose=False):
        self.X = None
        self.Y = None
        self.Z = None
        self.kwargs = {}
        self.verbose = verbose

        self.camera = None
        self.camera_aim = None

        self.xlim = None
        self.ylim = None
        self.zlim = None
        self.title = ""
        self.xticks = None
        self.yticks = None
        self.zticks = None
        self.xtick_labels = None
        self.ytick_labels = None
        self.ztick_labels = None

    # uses setattr to mimic the ax.set(xlim=[], ylim=[], title=[]) etc of matplotlib
    def set(self, **kwargs):
        for (key, val) in kwargs.items():
            setattr(self, key, val)

    def set_xticklabels(self, xticks=None, xtick_labels=None):
        self.xticks = xticks
        if xtick_labels is None:
            xtick_labels = [str(x) for x in xticks]
        self.xtick_labels = xtick_labels

    def set_yticklabels(self, yticks=None, ytick_labels=None):
        self.yticks = yticks
        if ytick_labels is None:
            ytick_labels = [str(y) for y in yticks]
        self.ytick_labels = ytick_labels

    def set_zticklabels(self, zticks=None, ztick_labels=None):
        self.zticks = zticks
        if ztick_labels is None:
            ztick_labels = [str(z) for z in zticks]
        self.ztick_labels = ztick_labels

    def save(self):
        filename = SAVE_PATH
        bpy.context.scene.render.filepath = str(filename.absolute())
        bpy.ops.render.render(write_still=True)
        return

    def show(self):
        self.add_camera()
        self.add_axes()
        self.add_ticks()
        self.add_tick_labels()

    def auto_generate_axes(self):
        self.xlim = [np.floor(np.min(self.X)), np.ceil(np.max(self.X))]
        self.ylim = [np.floor(np.min(self.Y)), np.ceil(np.max(self.Y))]
        self.zlim = [np.floor(np.min(self.Z)), np.ceil(np.max(self.Z))]

        self.xticks = np.linspace(self.xlim[0], self.xlim[1], 4)
        self.yticks = np.linspace(self.ylim[0], self.ylim[1], 4)
        self.zticks = np.linspace(self.zlim[0], self.zlim[1], 4)

        self.xtick_labels = [str(x) for x in self.xticks]
        self.ytick_labels = [str(y) for y in self.yticks]
        self.ztick_labels = [str(z) for z in self.zticks]

    def bar(self, X, Y, Z, mat=DEFAULTS['mat_bars'], **kwargs):
        self.X = X
        self.Y = Y
        self.Z = Z

        self.kwargs = kwargs

        self.auto_generate_axes()

        # mat = ColorGradient(name='test').add_to_scene()  # TODO: integrate better

        for (x, y, z) in zip(self.X.flatten(), self.Y.flatten(), self.Z.flatten()):
            # mat = FlatRBG.from_cmap(cmap='cividis', value=z, vmax=-1, vmin=1).add_to_scene()  # TODO: integrate better

            CubePrimitive(p=(x, y, 0), height=z, xy_scale=0.9, mat=mat).add_to_scene()
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            if check(kwargs, 'wireframe'):
                if self.verbose: print('adding a wireframe')
                bpy.ops.object.modifier_add(type='WIREFRAME')

            if check(self.kwargs, 'bevel'):
                if self.verbose: print('adding a bevel')
                bpy.ops.object.modifier_add(type='BEVEL')
                bpy.context.object.modifiers["Bevel"].width = 0.03
                bpy.context.object.modifiers["Bevel"].segments = 10

    def scatter(self, X, Y, Z, S, mat=DEFAULTS['mat_bars'], **kwargs):
        self.X = X
        self.Y = Y
        self.Z = Z

        self.kwargs = kwargs
        self.auto_generate_axes()
        for i, (x, y, z, s) in enumerate(zip(self.X.flatten(), self.Y.flatten(), self.Z.flatten(), S.flatten())):
            mat = FlatRBG.from_cmap(cmap='plasma', value=s, vmax=0, vmin=1).add_to_scene()  # TODO: integrate better

            SpherePrimitive(p=(x, y, z), scale=s, mat=mat).add_to_scene()


    def add_axes(self, mat=DEFAULTS['mat_axes']):
        t = 0.1
        borders = {
            'xy_bottom': True,
            'xy_top': True,
            'xy_left': True,
            'xy_right': True,
            'xz_corner': True,
        }
        if borders['xy_bottom']:
            LinePrimitive(p1=(self.xlim[0], self.ylim[0], 0),
                          p2=(self.xlim[1], self.ylim[0], 0),
                          plane='xy', thickness=t, mat=mat).add_to_scene()
        if borders['xy_left']:
            LinePrimitive(p1=(self.xlim[0], self.ylim[0], 0),
                          p2=(self.xlim[0], self.ylim[1], 0),
                          plane='xy', thickness=t, mat=mat).add_to_scene()
        if borders['xy_top']:
            LinePrimitive(p1=(self.xlim[0], self.ylim[1], 0),
                          p2=(self.xlim[1], self.ylim[1], 0),
                          plane='xy', thickness=t, mat=mat).add_to_scene()
        if borders['xy_right']:
            LinePrimitive(p1=(self.xlim[1], self.ylim[0], 0),
                          p2=(self.xlim[1], self.ylim[1], 0),
                          plane='xy', thickness=t, mat=mat).add_to_scene()

        if borders['xz_corner']:
            LinePrimitive(p1=(self.xlim[0], self.ylim[1], self.zlim[0]),
                          p2=(self.xlim[0], self.ylim[1], self.zlim[1]),
                          plane='xz', thickness=t, mat=mat).add_to_scene()
        return

    def add_ticks(self):
        TICK_LENGTH = 0.3
        for xtick in self.xticks:
            LinePrimitive(p1=(xtick, self.ylim[0], 0),
                          p2=(xtick, self.ylim[0]-TICK_LENGTH, 0),
                          plane='xy', thickness=0.2, mat=DEFAULTS['mat_axes']).add_to_scene()
        for ytick in self.yticks:
            LinePrimitive(p1=(self.xlim[0], ytick, 0),
                          p2=(self.xlim[0]-TICK_LENGTH, ytick, 0),
                          plane='xy', thickness=0.2, mat=DEFAULTS['mat_axes']).add_to_scene()
        return


    def add_tick_labels(self):
        XTICKBASE, YTICKBASE = 2 * [-0.8]
        for xi, xtick in zip(self.xticks, self.xtick_labels):
            FontPrimitive(text=str(xtick), p=(xi, XTICKBASE, 0)).add_to_scene()
        for yi, ytick in zip(self.yticks, self.ytick_labels):
            FontPrimitive(text=str(ytick), p=(YTICKBASE, yi, 0)).add_to_scene()
        return

    def add_camera(self, type="PERSP"):
        CameraPrimitive(loc=(4, 4, 0), camera_aim_loc=(4, 4, 0), type=type).add_to_scene()



