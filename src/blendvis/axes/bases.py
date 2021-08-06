import bpy
import copy
import numpy as np

# from blendvis import DEFAULTS, SAVE_PATH


class _Figure:
    """

    """
    def __init__(self, figsize=(1920, 1080), scale=1.0):
        self.axes = []

    def add_axes(self, axs):
        self.axes.append(axs)




class _Axes:
    """
    Holds some lower level functions for transforming between worlds
    """

    def __init__(self):

        self._bxlim = (0, 10)
        self._bylim = (0, 10)
        self._bzlim = (-1, 1)

        self._xlim = None
        self._ylim = None
        self._zlim = None
        return

    def trans_scene(self, x=None, y=None, z=None):
        # converts from data coordinates (xlim/ylim/zlim) to Blender cooredinates (bxlim/bylim/bzlim)
        xb, yb, zb = None, None, None
        if x is not None:
            xb = (x - self._xlim[0]) / (self._xlim[1] - self._xlim[0]) * (self._bxlim[1] - self._bxlim[0]) + self._bxlim[0]
        if y is not None:
            yb = (y - self._ylim[0]) / (self._ylim[1] - self._ylim[0]) * (self._bylim[1] - self._bylim[0]) + self._bylim[0]
        if z is not None:
            zb = (z - self._zlim[0]) / (self._zlim[1] - self._zlim[0]) * (self._bzlim[1] - self._bzlim[0]) + self._bzlim[0]
        return [xb, yb, zb]

    def trans_data(self, x=None, y=None, z=None):
        # converts from Blender coordinates (bxlim/bylim/bzlim) to data coordinates (based on xlim/ylim/zlim)
        xd, yd, zd = None, None, None
        if z is not None:
            xd = (x - self._bxlim[0]) / (self._bxlim[1] - self._bxlim[0]) * (self._xlim[1] - self._xlim[0]) + self._xlim[0]
        if z is not None:
            yd = (y - self._bylim[0]) / (self._bylim[1] - self._bylim[0]) * (self._ylim[1] - self._ylim[0]) + self._ylim[0]
        if z is not None:
            zd = (z - self._bzlim[0]) / (self._bzlim[1] - self._bzlim[0]) * (self._zlim[1] - self._zlim[0]) + self._zlim[0]
        return [xd, yd, zd]

    @staticmethod
    def auto_tick(tmin, tmax, nticks=6):
        # finds a nice division of ticks lines based on upper and lower boundaries
        # https://stackoverflow.com/questions/326679/choosing-an-attractive-linear-scale-for-a-graphs-y-axis
        range_ = 1.1 * (tmax - tmin)

        unrounded_tickrange = range_ / (nticks)
        x = np.ceil(np.log10(unrounded_tickrange))
        pow10x = np.power(10, x)
        rounded_tickrange = np.ceil(unrounded_tickrange / pow10x) * pow10x

        tmin_new = rounded_tickrange * np.floor(tmin / rounded_tickrange)
        tmax_new = tmin_new + rounded_tickrange * (nticks - 1)

        ticks = [tmin_new + i * rounded_tickrange for i in range(nticks)]
        return (tmin_new, tmax_new), ticks

    """
    Set up properties of the Axes class with getter/setter functions
    """
    @property
    def xlim(self):
        return

    @xlim.getter
    def xlim(self):
        return self._xlim

    @xlim.setter
    def xlim(self, _xlim):
        self._xlim = _xlim
        return

    # ylim as a property
    @property
    def ylim(self):
        return

    @ylim.getter
    def ylim(self):
        return self._ylim

    @ylim.setter
    def ylim(self, _ylim):
        self._ylim = _ylim
        return

    # zlim as a property
    @property
    def zlim(self):
        return

    @zlim.getter
    def zlim(self):
        return self._zlim

    @zlim.setter
    def zlim(self, _zlim):
        self._zlim = _zlim
        return
