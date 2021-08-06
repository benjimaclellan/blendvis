from blendvis.materials import FlatRGB, GreasePencil
from blendvis import rcParams

DEFAULTS = {
    'mat_axes': FlatRGB(name="axes", rgba=3 * [0.1] + [1]).add_to_scene(),
    'mat_bars': FlatRGB(name="boxes", rgba=(1, 1, 1, 1)).add_to_scene(),
    'mat_font': FlatRGB(name="fonts", rgba=(0, 0, 0, 1)).add_to_scene(),
    'black': FlatRGB(name="black", rgba=(0, 0, 0, 1)).add_to_scene(),
    'red': FlatRGB(name="red", rgba=(1, 0, 0, 1)).add_to_scene(),
    'blue': FlatRGB(name="blue", rgba=(0, 0, 1, 1)).add_to_scene(),
    'green': FlatRGB(name="green", rgba=(0, 1, 0, 1)).add_to_scene(),
}