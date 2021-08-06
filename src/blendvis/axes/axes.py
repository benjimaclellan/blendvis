import bpy
import numpy as np

from blendvis.primitives import FontPrimitive, CubePrimitive, \
    CameraPrimitive, SpherePrimitive, CurvePrimitive, GreasePencilPrimitive
from blendvis.axes.bases import _Axes
from blendvis import DEFAULTS, SAVE_PATH


def check(kwargs, key):
    if key in kwargs.keys():
        if kwargs[key]:
            return True
    return False


# add in the collections that sort the objects in the scene
def init_collections():
    for coll in ['MAIN', 'FONTS', 'LINES', 'MESHES', 'CAMERA', "CURVES", "PENCILS", "LATEX"]:
        c = bpy.data.collections.new(coll)
        bpy.context.scene.collection.children.link(c)


def remove_all_other_scenes(scene_keep=None):
    for scene in bpy.data.scenes:
        if not (scene == scene_keep):
            bpy.data.scenes.remove(scene)


def remove_all_other_worlds(world_keep=None):
    for world in bpy.data.worlds:
        if not (world == world_keep):
            bpy.data.worlds.remove(world)



class Axes(_Axes):
    def __init__(self, name="My BlendVis Figure", verbose=False):
        super().__init__()

        self.render_list = []

        self.kwargs = {}
        self.verbose = verbose
        self.name = name

        self.camera = None
        self.camera_aim = None

        self.title = ""
        self.xticks = None
        self.yticks = None
        self.zticks = None
        self.xtick_labels = None
        self.ytick_labels = None
        self.ztick_labels = None

        self.scene = bpy.data.scenes.new("BVIS Scene")
        remove_all_other_scenes(self.scene)

        layer = self.scene.view_layers.new(name='BVIS View Layer')
        bpy.context.window.view_layer = layer

        remove_all_other_worlds()
        self.world = bpy.data.worlds.new("BVIS World")
        self.world.use_nodes = True
        self.world.node_tree.nodes["Background"].inputs[0].default_value = (0.999985, 0.999985, 0.999985, 1)
        bpy.context.scene.world = self.world

        init_collections()

    def _update_lim(self, t, tlim, ticks):
        tmin = np.min(t)
        tmax = np.max(t)

        (tmin_new, tmax_new), ticks_new = self.auto_tick(tmin, tmax, nticks=6)
        # print(tmin, tmax, tmin_new, tmax_new, tlim, ticks)

        if tlim is None:
            return (tmin_new, tmax_new), ticks_new
        elif tmax_new - tmin_new > (tlim[1] - tlim[0]):
            return (tmin_new, tmax_new), ticks_new
        else:
            return tlim, ticks

    def update_lims(self, x=None, y=None, z=None):
        self.xlim, self.xticks = self._update_lim(x, self.xlim, self.xticks)
        self.ylim, self.yticks = self._update_lim(y, self.ylim, self.yticks)
        self.zlim, self.zticks = self._update_lim(z, self.zlim, self.zticks)
        # print(self.xlim, self.ylim, self.zlim)
        # raise NotImplementedError  # update the estimated axis-limits and tick markings

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
        self.xtick_labels = [str(x) for x in self.xticks]
        self.ytick_labels = [str(y) for y in self.yticks]
        self.ztick_labels = [str(z) for z in self.zticks]

        for render_func in self.render_list:
            render_func()

        self.add_camera()
        self.add_axes()
        self.add_ticks()
        self.add_tick_labels()
        self.add_major_grid()


    """
    def decorator(self, func, *args, **kwargs):
        self.render_list.append(func(*args, **args)
    """

    def bar(self, x=None, y=None, z=None, mat=DEFAULTS['mat_bars'], **kwargs):
        def add_to_scene(self, x=None, y=None, z=None, mat=None, **kwargs):
            x, y, z = self.trans_scene(x, y, z)
            # ZBASE = 0
            _, _, ZBASE = self.trans_scene(0, 0, 0)
            # mat = ColorGradient(name='test').add_to_scene()  # TODO: integrate better
            for (xi, yi, zi) in zip(x.flatten(), y.flatten(), z.flatten()):
                # mat = FlatRBG.from_cmap(cmap='cividis', value=z, vmax=-1, vmin=1).add_to_scene()  # TODO: integrate better
                CubePrimitive(p=(xi, yi, ZBASE), height=zi, xy_scale=0.9, mat=mat).add_to_scene()
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                if check(kwargs, 'wireframe'):
                    if self.verbose: print('adding a wireframe')
                    bpy.ops.object.modifier_add(type='WIREFRAME')

                if check(self.kwargs, 'bevel'):
                    if self.verbose: print('adding a bevel')
                    bpy.ops.object.modifier_add(type='BEVEL')
                    bpy.context.object.modifiers["Bevel"].width = 0.03
                    bpy.context.object.modifiers["Bevel"].segments = 10
            return

        self.update_lims(x, y, z)
        self.render_list.append(lambda: add_to_scene(self, x=x, y=y, z=z, mat=mat, **kwargs))

    # @update_and_queue
    def scatter(self, x=None, y=None, z=None, s=0.02, mat=DEFAULTS['mat_bars'], **kwargs):
        def add_to_scene(self, x=None, y=None, z=None, s=0.02, mat=DEFAULTS['mat_bars'], **kwargs):
            # convert to Blender's coordinates. This should be done here, at final render (when lims have been finalized)
            x, y, z = self.trans_scene(x, y, z)

            for i, (xi, yi, zi) in enumerate(zip(x.flatten(), y.flatten(), z.flatten())):
                if type(s) is float:
                    si = s
                elif type(s) is np.ndarray:
                    si = s[i]
                else:
                    raise ValueError("scatter point size 's' must be a float or a numpy array")
                # mat = FlatRBG.from_cmap(cmap='plasma', value=s, vmax=0, vmin=1).add_to_scene()  # TODO: integrate better
                # SpherePrimitive(p=(self.trans_data(x), self.trans_data(y), self.trans_data(z)), scale=s, mat=mat).add_to_scene()
                print(self)
                SpherePrimitive(p=(xi, yi, zi), scale=si, mat=mat).add_to_scene()
            return

        self.update_lims(x, y, z)
        self.render_list.append(lambda: add_to_scene(self, x=x, y=y, z=z, s=s, mat=mat, **kwargs))

    def line(self, x=None, y=None, z=None, mat=DEFAULTS['black'], **kwargs):
        def add_to_scene(self, x=None, y=None, z=None, mat=DEFAULTS['mat_bars'], **kwargs):
            x, y, z = self.trans_scene(x, y, z)
            CurvePrimitive(x=x, y=y, z=z, mat=mat).add_to_scene()
            return

        self.update_lims(x, y, z)
        self.render_list.append(lambda: add_to_scene(self, x=x, y=y, z=z, mat=mat, **kwargs))

    def add_axes(self):
        g = GreasePencilPrimitive(pressure=50)

        g.add_stroke([self.trans_scene(self.xlim[0], self.ylim[0], self.zlim[0]),
                      self.trans_scene(self.xlim[0], self.ylim[1], self.zlim[0]),
                      self.trans_scene(self.xlim[1], self.ylim[1], self.zlim[0]),
                      self.trans_scene(self.xlim[1], self.ylim[0], self.zlim[0]),
                      self.trans_scene(self.xlim[0], self.ylim[0], self.zlim[0]),
                      ])

        g.add_stroke([self.trans_scene(self.xlim[0], self.ylim[1], self.zlim[0]),
                      self.trans_scene(self.xlim[0], self.ylim[1], self.zlim[1]),
                      ])
        g.add_stroke([self.trans_scene(self.xlim[1], self.ylim[1], self.zlim[0]),
                      self.trans_scene(self.xlim[1], self.ylim[1], self.zlim[1]),
                      ])
        g.add_stroke([self.trans_scene(self.xlim[1], self.ylim[0], self.zlim[0]),
                      self.trans_scene(self.xlim[1], self.ylim[0], self.zlim[1]),
                      ])
        g.add_to_scene()

    def add_ticks(self):
        g = GreasePencilPrimitive(pressure=50)

        TICK_LENGTH = 0.3
        for xtick in self.xticks:
            g.add_stroke([self.trans_scene(xtick, self.ylim[0], self.zlim[0]),
                          self.trans_scene(xtick, self.ylim[0]-TICK_LENGTH, self.zlim[0])
                          ])
        for ytick in self.yticks:
            g.add_stroke([self.trans_scene(self.xlim[0], ytick, self.zlim[0]),
                          self.trans_scene(self.xlim[0] - TICK_LENGTH, ytick, self.zlim[0])
                          ])
        g.add_to_scene()
        return

    def add_major_grid(self):
        g = GreasePencilPrimitive(pressure=30)
        for xtick in self.xticks:
            g.add_stroke([self.trans_scene(xtick, self.ylim[0], self.zlim[0]),
                          self.trans_scene(xtick, self.ylim[1], self.zlim[0])
                          ])
        for ytick in self.yticks:
            g.add_stroke([self.trans_scene(self.xlim[0], ytick, self.zlim[0]),
                          self.trans_scene(self.xlim[1], ytick, self.zlim[0])
                          ])
        g.add_to_scene()
        return

    def add_tick_labels(self):
        # XTICKBASE, YTICKBASE = 2 * [-0.8]
        OFFSET = -0.8
        for xi, xtick in zip(self.xticks, self.xtick_labels):
            p = self.trans_scene(xi, self.ylim[0], self.zlim[0])
            print(type(p))
            print(p)
            p[1] += OFFSET
            FontPrimitive(text=str(xtick), p=p).add_to_scene()
        for yi, ytick in zip(self.yticks, self.ytick_labels):
            p = self.trans_scene(self.xlim[0], yi, self.zlim[0])
            p[0] += OFFSET
            FontPrimitive(text=str(ytick), p=p).add_to_scene()
        return

    def add_camera(self, azimuth=45, type="PERSP"):
        camera_aim_loc = ((self._bxlim[1] + self._bxlim[0]) / 2,
                          (self._bylim[1] + self._bylim[0]) / 2,
                          (self._bzlim[1] + self._bzlim[0]) / 2)
        CameraPrimitive(radius=20, camera_aim_loc=camera_aim_loc, type=type).add_to_scene()



