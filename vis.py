# inspired by https://discourse.vtk.org/t/working-with-a-hdf-file-in-vtk/11233/5

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkRenderingCore import (

    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)
import vtk

colors = vtkNamedColors()

file_name = 'test.hdf'

# Read the source file.
reader = vtk.vtkHDFReader()
reader.SetFileName(file_name)
reader.Update()

outDS = reader.GetOutput()
# outDS.GetPointData().SetScalars(outDS.GetPointData().GetArray("test"))

# print(dir(outDS))

# print(outDS.GetCellData())
# print(outDS.GetPointData())
# print(outDS.GetPoints())
# print(outDS.GetCells())