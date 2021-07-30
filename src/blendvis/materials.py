import bpy


class Material:
    def __init__(self, name="Material"):
        self.name = name


class FlatRBG(Material):
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
