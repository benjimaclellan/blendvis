import bpy


class Material:
    def __init__(self, name="Material"):
        self.name = name


class GreasePencil(Material):

    def __init__(self, name="blendvis-gp", rgba=(0, 1, 0, 1)):
        self.name = name
        self.rgba = rgba

    def add_to_scene(self):
        mat = bpy.data.materials.new("GPMaterial")
        print("great gatsby" + str(mat))
        return mat


class FlatRGB(Material):
    def __init__(self, name="blendvis-rgba", rgba=(0, 1, 0, 1)):
        self.name = name
        self.rgba = rgba

    @classmethod
    def from_cmap(cls, cmap='cividis', value=0, vmin=0, vmax=1):
        import matplotlib.pyplot as plt
        cm = plt.get_cmap(cmap)
        rgba = cm((value - vmin)/(vmax - vmin))
        return cls(name=cmap+str(value), rgba=rgba)

    def add_to_scene(self):
        mat = bpy.data.materials.new(name=self.name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        node_bsdf = nodes.get("Principled BSDF")
        node_bsdf.inputs[0].default_value = self.rgba
        return mat


class ColorGradient(Material):
    def __init__(self, name="blendvis-zgradient"):
        self.name = name

    def add_to_scene(self):
        mat = bpy.data.materials.new(name=self.name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes

        # add all the nodes
        node_bsdf = nodes.get("Principled BSDF")
        node_text_coords = nodes.new(type="ShaderNodeTexCoord")
        node_mapping = nodes.new(type="ShaderNodeMapping")
        node_sepxyz = nodes.new(type="ShaderNodeSeparateXYZ")
        node_colorramp = nodes.new(type="ShaderNodeValToRGB")
        # node_mat_out = nodes.get("Material Output")

        node_colorramp.color_ramp.elements[0].color = (0, 0, 0, 1)
        node_colorramp.color_ramp.elements[1].color = (1, 1, 0, 1)

        # link the nodes
        links = mat.node_tree.links
        links.new(node_text_coords.outputs[0], node_mapping.inputs[0])
        links.new(node_mapping.outputs[0], node_sepxyz.inputs[0])
        links.new(node_sepxyz.outputs[2], node_colorramp.inputs[0])
        links.new(node_colorramp.outputs[0], node_bsdf.inputs[0])
        return mat


class ZGradient(Material):
    def __init__(self, name="blendvis-zgradient", vmin=0, vmax=1):
        self.name = name
        self.vmin = vmin
        self.vmax = vmax

    def add_to_scene(self):
        mat = bpy.data.materials.new(name=self.name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes

        # add all the nodes
        node_geo_coords = nodes.new(type="ShaderNodeNewGeometry")
        node_geo_coords.location = (-1000, 0)

        node_sepxyz = nodes.new(type="ShaderNodeSeparateXYZ")
        node_sepxyz.location = (-800, 0)

        node_math1 = nodes.new(type="ShaderNodeMath")
        node_math1.operation = "SUBTRACT"
        node_math1.location = (-600, 0)

        node_math2 = nodes.new(type="ShaderNodeMath")
        node_math2.operation = "DIVIDE"
        node_math2.location = (-400, 0)

        node_vmin = nodes.new(type="ShaderNodeValue")
        node_vmin.outputs[0].default_value = self.vmin
        node_vmin.location = (-800, -200)

        node_vmax = nodes.new(type="ShaderNodeValue")
        node_vmax.outputs[0].default_value = self.vmax
        node_vmax.location = (-800, -400)

        node_range = nodes.new(type="ShaderNodeMath")
        node_range.operation = "SUBTRACT"
        node_range.location = (-600, -300)

        node_colorramp = nodes.new(type="ShaderNodeValToRGB")
        node_colorramp.location = (-200, 0)

        node_bsdf = nodes.get("Principled BSDF")
        node_bsdf.location = (200, 0)

        node_mat_out = nodes.get("Material Output")
        node_mat_out.location = (600, 0)

        node_colorramp.color_ramp.elements[0].color = (0.120064, 0.268282, 0.64215, 1)
        node_colorramp.color_ramp.elements[1].color = (0.209783, 1, 0.257535, 1)

        # link the nodes
        links = mat.node_tree.links

        # calculate range
        links.new(node_vmax.outputs[0], node_range.inputs[0])
        links.new(node_vmin.outputs[0], node_range.inputs[1])

        # map the z-value to a range [0, 1] (based on vmax, vmin) for the colorramp
        # TODO: convert between data coords and blender coords
        links.new(node_geo_coords.outputs[0], node_sepxyz.inputs[0])
        links.new(node_sepxyz.outputs[2], node_math1.inputs[0])
        links.new(node_vmin.outputs[0], node_math1.inputs[1])

        links.new(node_math1.outputs[0], node_math2.inputs[0])
        links.new(node_range.outputs[0], node_math2.inputs[1])

        links.new(node_math2.outputs[0], node_colorramp.inputs[0])
        links.new(node_colorramp.outputs[0], node_bsdf.inputs[0])
        return mat
