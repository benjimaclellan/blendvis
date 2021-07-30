import bpy
import copy
from math import radians
import pathlib

from blendvis import DEFAULTS


class Primitive:
    collection = "MAIN"

    def __init__(self):
        return

    def add_material(self, ob, mat):
        if type(mat) is str:
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


class CameraPrimitive(Primitive):
    collection = "CAMERA"

    def __init__(self, loc=(4, 4, 0), camera_aim_loc=(4, 4, 0), type="PERSP"):
        self.loc = loc
        self.camera_aim_loc = camera_aim_loc
        self.type = type
        self.camera_aim = None
        self.camera = None

    def add_to_scene(self):

        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 00), scale=(1, 1, 1))
        self.camera_aim = bpy.context.active_object
        self.link_collection(self.camera_aim)

        self.camera_aim.location = [4, 4, 0]

        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(-6, -6, 7),
                                  rotation=(radians(65), radians(0), radians(-45)), scale=(1, 1, 1))
        self.camera = bpy.context.active_object
        self.camera.data.type = self.type
        bpy.ops.object.constraint_add(type='TRACK_TO')
        bpy.context.object.constraints["Track To"].target = self.camera_aim
        bpy.ops.transform.translate(value=(0, 0, 10), orient_type='LOCAL')
        bpy.context.scene.camera = self.camera
        self.link_collection(self.camera)

        return

