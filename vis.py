# inspired by https://discourse.vtk.org/t/working-with-a-hdf-file-in-vtk/11233/5

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkRenderingCore import (

    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)
import vtk

colors = vtkNamedColors()

file_name = 'test.hdf5'

# Read the source file.
reader = vtk.vtkHDFReader()
reader.SetFileName(file_name)
reader.Update()