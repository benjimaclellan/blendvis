from blendvis.materials import FlatRBG, GreasePencil
from blendvis import rcParams

DEFAULTS = {
    'mat_axes': FlatRBG(name="axes", rgba=3 * [0.1] + [1]).add_to_scene(),
    'mat_bars': FlatRBG(name="boxes", rgba=(1, 1, 1, 1)).add_to_scene(),
    'mat_font': FlatRBG(name="fonts", rgba=(0, 0, 0, 1)).add_to_scene(),
    'black': FlatRBG(name="black", rgba=(0, 0, 0, 1)).add_to_scene(),
    'red': FlatRBG(name="red", rgba=(1, 0, 0, 1)).add_to_scene(),
    'blue': FlatRBG(name="blue", rgba=(0, 0, 1, 1)).add_to_scene(),
    'green': FlatRBG(name="green", rgba=(0, 1, 0, 1)).add_to_scene(),
}