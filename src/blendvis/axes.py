import bpy
import copy
from math import radians
import pathlib

DEFAULTS = {'mat_axes': "Black", 'mat_bars': "Boxes", 'mat_font': "Black"}
SAVE_PATH = pathlib.Path(r"C:\Users\benjamin\OneDrive - University of Waterloo\Documents\IQC - Projects\Code\blendvis\examples\renders\3d-barplot.png")

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

    def clear(self):
        # remove all objects
        for object in bpy.data.objects:
            object.select_set(True)
            bpy.data.objects.remove(object, do_unlink=True)

    def save(self):
        filename = SAVE_PATH
        bpy.context.scene.render.filepath = str(filename.absolute())
        bpy.ops.render.render(write_still=True)
        return

    def barplot(self, X, Y, Z, bevel=True, wireframe=False, mat=DEFAULTS['mat_bars']):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.kwargs['bevel'] = bevel
        self.kwargs['wireframe'] = wireframe

        for (x, y, z) in zip(self.X.flatten(), self.Y.flatten(), self.Z.flatten()):
            CubePrimative(p=(x, y, 0), height=z, xy_scale=0.9, mat=mat).add_to_scene()
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
        LinePrimative(p1=(xlim[0], ylim[0], 0), p2=(xlim[1], ylim[0], 0), plane='xy', thickness=0.2, mat=mat).add_to_scene()
        LinePrimative(p1=(xlim[0], ylim[0], 0), p2=(xlim[0], ylim[1], 0), plane='xy', thickness=0.2, mat=mat).add_to_scene()
        return


    def add_tick_labels(self, x=[0, 1], xtick_labels=None, y=[0, 1], ytick_labels=None):
        XTICKBASE, YTICKBASE = 2 * [-0.8]
        if xtick_labels is None:
            xtick_labels = copy.copy(x)
        if ytick_labels is None:
            ytick_labels = copy.copy(y)

        for xi, xtick in zip(x, xtick_labels):
            FontPrimative(text=str(xtick), p=(xi, XTICKBASE, 0)).add_to_scene()
        for yi, ytick in zip(y, ytick_labels):
            FontPrimative(text=str(ytick), p=(YTICKBASE, yi, 0)).add_to_scene()
        return None

    def add_camera(self, type='PERSPECTIVE'):
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 00), scale=(1, 1, 1))
        self.camera_aim = bpy.context.active_object

        # self.camera_aim.data.location = [4, 4, 0]
        self.camera_aim.location = [4, 4, 0]
        self.camera = bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(-6, -6, 7),
                                                rotation=(radians(65), radians(0), radians(-45)), scale=(1, 1, 1))
        print(self.camera)
        bpy.ops.object.constraint_add(type='TRACK_TO')
        bpy.context.object.constraints["Track To"].target = self.camera_aim
        bpy.ops.transform.translate(value=(0, 0, 10), orient_type='LOCAL')
        # bpy.context.scene.camera = self.camera
        bpy.context.scene.camera = bpy.data.objects["Camera"]



class Primative:
    def __init__(self):
        return

    def add_material(self, ob, mat):
        mat = bpy.data.materials.get(mat)
        if ob.data.materials:
            # assign to 1st material slot
            ob.data.materials[0] = mat
        else:
            # no slots
            ob.data.materials.append(mat)
        return


class FontPrimative(Primative):
    def __init__(self, text="text", p=(0, 0, 0), mat=DEFAULTS['mat_font']):
        self.text = text
        self.p = p
        self.mat = mat

    def add_to_scene(self):
        font_curve = bpy.data.curves.new(type="FONT", name="Font Curve")
        font_curve.body = self.text

        font_obj = bpy.data.objects.new(name="Font Object", object_data=font_curve)
        bpy.context.scene.collection.objects.link(font_obj)
        # bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

        font_obj.location = (self.p[0], self.p[1], self.p[2])
        font_obj.data.align_x = "CENTER"

        if self.mat is not None:
            self.add_material(font_obj, self.mat)


class LinePrimative(Primative):
    def __init__(self, p1=(0, 0, 0), p2=(1, 0, 0), plane='xy', thickness=0.2, mat=None):
        self.p1 = p1
        self.p2 = p2
        self.plane = plane
        self.thickness = thickness
        self.mat = mat

    def add_to_scene(self):
        xmid = (self.p2[0] + self.p1[0]) / 2
        ymid = (self.p2[1] + self.p1[1]) / 2
        zmid = (self.p2[2] + self.p1[2]) / 2

        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0),
                                         scale=(1, 1, 1))
        ob = bpy.context.active_object

        ob.scale = [self.thickness + (self.p2[0] - self.p1[0]),
                    self.thickness + (self.p2[1] - self.p1[1]),
                    self.thickness + (self.p2[2] - self.p1[2])]
        ob.location = [xmid, ymid, zmid]

        if self.mat is not None:
            self.add_material(ob, self.mat)
        return None



class CubePrimative(Primative):
    def __init__(self, p=(0, 0, 0), height=1.0, xy_scale=0.9, mat=None):
        self.p = p
        self.xy_scale = xy_scale
        self.height = height
        self.mat = mat

    # add a cube and move/scale it based on input data point
    def add_to_scene(self):
        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0),
                                        scale=(1, 1, 1))
        ob = bpy.context.active_object

        bpy.context.scene.cursor.location = (0, 0, -0.5)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        ob.location = (self.p[0], self.p[1], self.p[2])
        ob.scale = (self.xy_scale, self.xy_scale, self.height)

        if self.mat is not None:
            self.add_material(ob, self.mat)
        return



class Material:
    def __init__(self):
        self.a = 1

