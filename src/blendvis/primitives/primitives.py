import bpy
import copy
from math import radians
import pathlib
import numpy as np

from blendvis import DEFAULTS, MAIN_FONT, DEFAULT_GP, rcParams, DEFAULT_FONT

bpy.ops.font.open(filepath="//..\\..\\..\\..\\..\\..\\..\\..\\WINDOWS\\Fonts\\couri.ttf", relative_path=True)
MAIN_FONT = bpy.data.fonts[len(bpy.data.fonts)-1]


class Primitive:
    collection = "MAIN"

    def __init__(self):
        return

    def add_material(self, ob, mat):
        if type(mat) is str:
            if mat in DEFAULTS.keys():
                mat = DEFAULTS[mat]
            else:
                mat = bpy.data.materials.get(mat)
        elif type(mat) is bpy.types.Material:
            pass
        else:
            raise TypeError("Not a material")

        if ob.data.materials:
            # assign to 1st material slot
            ob.data.materials[0] = mat
        else:
            # no slots
            ob.data.materials.append(mat)
        return

    def link_collection(self, ob):
        for c in ob.users_collection:  # unlink from all past collections
            c.objects.unlink(ob)
        bpy.data.collections[self.collection].objects.link(ob)  # link to desired collection
        bpy.context.view_layer.objects.active = ob
        return


class FontPrimitive(Primitive):
    collection = 'FONTS'

    def __init__(self, text="text", p=(0, 0, 0), mat=None):
        self.text = text
        self.p = p
        self.mat = mat if mat is not None else DEFAULT_FONT

    def add_to_scene(self):
        font_curve = bpy.data.curves.new(type="FONT", name="Font Curve")
        font_curve.body = self.text
        font_curve.align_x = "CENTER"
        font_curve.align_y = "CENTER"
        font_curve.font = MAIN_FONT

        font_obj = bpy.data.objects.new(name="Font Object", object_data=font_curve)
        font_obj.location = self.p
        self.link_collection(font_obj)

        if self.mat is not None:
            self.add_material(font_obj, self.mat)


class LinePrimitive(Primitive):
    collection = 'LINES'
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

        # orient the 2d plane in 3d space
        if self.plane == 'xy':
            pass
        elif self.plane == 'yz':
            ob.rotation_euler = (radians(0), radians(90), radians(0))
        elif self.plane == 'xz':
            ob.rotation_euler = (radians(90), radians(0), radians(0))
        else:
            raise TypeError("Not a proper orientation for 2d plane in 3d space. Choose 'xy', 'yz', or 'xz'")
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

        ob.scale = [self.thickness + (self.p2[0] - self.p1[0]),
                    self.thickness + (self.p2[1] - self.p1[1]),
                    self.thickness + (self.p2[2] - self.p1[2])]
        ob.location = [xmid, ymid, zmid]

        self.link_collection(ob)

        if self.mat is not None:
            self.add_material(ob, self.mat)
        return None


class CubePrimitive(Primitive):
    collection = 'MESHES'

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

        ob.location = self.p
        ob.scale = (self.xy_scale, self.xy_scale, self.height)

        self.link_collection(ob)

        if self.mat is not None:
            self.add_material(ob, self.mat)
        return


class SpherePrimitive(Primitive):
    collection = 'MESHES'
    type = "uv"  # "ico" or "uv"

    def __init__(self, p=(0, 0, 0), scale=1, mat=None):
        self.p = p
        self.scale = scale
        self.mat = mat

    def add_to_scene(self):
        if self.type == 'ico':
            bpy.ops.mesh.primitive_ico_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, -0.5),
                                                  scale=(1, 1, 1))
        elif self.type == 'uv':
            bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, -0.5),
                                                 scale=(1, 1, 1))
        ob = bpy.context.active_object

        ob.location = self.p
        ob.scale = 3 * [self.scale]

        self.link_collection(ob)

        if self.mat is not None:
            self.add_material(ob, self.mat)
        return


class CameraPrimitive(Primitive):
    collection = "CAMERA"

    def __init__(self, radius=10, azimuthal=65, altitude=-135, camera_aim_loc=(4, 4, 0), type="PERSP"):
        self.camera_aim_loc = camera_aim_loc
        self.radius = radius
        self.azimuthal = np.radians(azimuthal)
        self.altitude = np.radians(altitude)
        self.type = type
        self.camera_aim = None
        self.camera = None

    def add_to_scene(self):
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD',
                                 location=self.camera_aim_loc, scale=(1, 1, 1))
        self.camera_aim = bpy.context.active_object
        self.link_collection(self.camera_aim)

        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW',
                                  location=(self.radius * np.sin(self.azimuthal) * np.cos(self.altitude),
                                            self.radius * np.sin(self.azimuthal) * np.sin(self.altitude),
                                            self.radius * np.cos(self.azimuthal)),
                                  scale=(1, 1, 1))
        self.camera = bpy.context.active_object
        self.camera.data.type = self.type

        bpy.ops.object.constraint_add(type='TRACK_TO')
        bpy.context.object.constraints["Track To"].target = self.camera_aim
        bpy.context.scene.camera = self.camera
        self.link_collection(self.camera)
        return


class CurvePrimitive(Primitive):
    type = "POLY"
    collection = "CURVES"

    def __init__(self, x=None, y=None, z=None, w=None, mat=None, cyclic=False, depth=0.05):
        self.x = x
        self.y = y
        self.z = z
        if w is None:
            self.w = np.ones_like(x)

        self.cyclic = cyclic
        self.depth = depth
        self.nurbs_weight = 1.0

        self.mat = mat

    def add_to_scene(self):
        # make a new curve
        def flatten(*args):
            c = np.empty(sum(len(arg) for arg in args))
            l = len(args)
            for i, arg in enumerate(args):
                c[i::l] = arg
            return c

        cu = bpy.data.curves.new(name="poly", type='CURVE')
        cu.dimensions = '3D'

        spline = cu.splines.new('POLY')  # poly type
        # spline is created with one point add more to match data
        spline.points.add(len(self.x) - 1)
        spline.points.foreach_set("co", flatten(self.x, self.y, self.z, self.w))

        ob = bpy.data.objects.new("Poly", cu)
        ob.data.bevel_depth = self.depth

        self.link_collection(ob)

        if self.mat is not None:
            self.add_material(ob, self.mat)


class GreasePencilPrimitive(Primitive):

    collection = "PENCILS"

    def __init__(self, pressure=100, mat=None):
        self.pressure = pressure
        self.strokes = []
        self.mat = mat if mat is not None else DEFAULT_GP

    def add_stroke(self, points=None):
        self.strokes.append(points)

    def add_to_scene(self):
        gp_data = bpy.data.grease_pencils.new("GPencil")
        gp_layer = gp_data.layers.new(name="GPLayer")
        gp_frame = gp_layer.frames.new(frame_number=0)

        for stroke in self.strokes:
            gp_stroke = gp_frame.strokes.new()
            gp_stroke.points.add(count=len(stroke))
            for i, point in enumerate(stroke):
                gp_stroke.points[i].co = point
                gp_stroke.points[i].strength = 20
                gp_stroke.points[i].pressure = self.pressure

        gp_mat = self.mat
        if not gp_mat.is_grease_pencil:
            bpy.data.materials.create_gpencil_data(gp_mat)
            gp_mat.grease_pencil.color = (0, 0, 0, 1)

        gp_data.materials.append(gp_mat)

        ob = bpy.data.objects.new("GPencilObject", gp_data)
        self.link_collection(ob)

