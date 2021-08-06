
from blendvis.axes import Axes

# TODO: figure out cyclic import issue - may need more structuring

def figure():
    return Figure(), Axes()

def subplots():
    return Figure(), Axes()



class Figure:
    """

    """
    def __init__(self, figsize=(1920, 1080), scale=1.0):
        self.axes = []


    def add_axes(self, axs):
        self.axes.append(axs)
