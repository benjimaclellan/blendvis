import bpy
import subprocess
import pathlib
import uuid
import os
import glob


from blendvis.primitives import Primitive
from blendvis import DEFAULTS, MAIN_FONT, DEFAULT_GP, rcParams, DEFAULT_FONT


class LatexPrimitive(Primitive):
    collection = "LATEX"

    def __init__(self, loc=(0, 0, 0), scale=100, mat=None):
        self.loc = loc
        self.scale = scale
        self.mat = mat if mat is not None else DEFAULT_FONT

        self.file = 'template.tex'
        self.tmp_name = pathlib.Path(str(uuid.uuid4()))

        self.inkscape_cmd = r"'C:\Program Files\Inkscape\bin\inkscape'"
        self.pdf2svg_cmd = r'"C:\Users\benjamin\Downloads\pdf2svg-windows-master\pdf2svg-windows-master\dist-64bits\pdf2svg.exe"'
        self.pdflatex_cmd = "pdflatex"

        self.template_file = pathlib.Path("template.tex")
        return

    def clean_up_tmp_files(self):
        _dir = pathlib.Path(__file__).parent.resolve()  # TODO use some packaging util to set paths
        for filename in glob.glob(str(_dir.joinpath('tmp').joinpath("*"))):
            os.remove(filename)
            print(filename)

    def render(self, text=r'$\vert HV \rangle$', **kwargs):

        kwargs = {'$__EQUATION__$': text}

        _dir = pathlib.Path(__file__).parent.resolve()  # TODO use some packaging util to set paths

        with open(_dir.joinpath(self.template_file), 'r') as file:
            text = file.read()

            for key, value in kwargs.items():
                text = text.replace(key, value)

            # tex_file_name = self.tmp_name.with_suffix(".tex")
            tmp_folder = _dir.joinpath('tmp')
            tex_file = tmp_folder.joinpath(self.tmp_name).with_suffix(".tex")

            with open(tex_file, "w") as tmp_file:
                tmp_file.write(text)

            # make pdf via pdflatex
            subprocess.call(f"{self.pdflatex_cmd} {self.tmp_name}.tex", shell=True, cwd=tmp_folder)

            # make svg using pdf2svg
            subprocess.call(f'{self.pdf2svg_cmd} {str(self.tmp_name.with_suffix(".pdf"))} {str(self.tmp_name.with_suffix(".svg"))}',
                            shell=True, cwd=tmp_folder)

    def add_to_scene(self):

        _dir = pathlib.Path(__file__).parent.resolve()  # TODO use some packaging util to set paths
        tmp_folder = _dir.joinpath('tmp')
        tex_file = tmp_folder.joinpath(self.tmp_name).with_suffix(".svg")

        start_objs = bpy.data.objects[:]
        bpy.ops.import_curve.svg(filepath=str(tex_file))
        new_curves = [o for o in bpy.data.objects if o not in start_objs]

        bpy.ops.object.select_all(action='DESELECT')
        for curve in new_curves:
            curve.select_set(True)

        bpy.context.view_layer.objects.active = new_curves[0]
        bpy.ops.object.join()

        ob = bpy.context.view_layer.objects.active
        ob.name = str(self.tmp_name)
        ob.location = self.loc
        ob.scale = 3 * [self.scale]

        self.add_material(ob, self.mat)

        self.clean_up_tmp_files()

