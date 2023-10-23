from dolfinx import cpp as _cpp
from dolfinx import fem, mesh
import numpy as np

from vtkmodules.vtkCommonDataModel import (
    VTK_TRIANGLE,
    VTK_VERTEX,
    vtkUnstructuredGrid
)

import vtkmodules
print(dir(vtkmodules))

# https://pyscience.wordpress.com/2014/09/06/numpy-to-vtk-converting-your-numpy-arrays-to-vtk-arrays-and-files/

# see:
# ./vtk-examples/src/Python/UnstructuredGrid/UGrid.py

def numpy_to_vtk():

    tri_points = np.array([[0,0,0],[0,1,0],[1,0,0],[1,1,0]], dtype=np.float64)
    triangles = np.array([[0,1,3], [0,2,3]], dtype=np.int64)

    from vtkmodules.vtkCommonCore import vtkPoints, vtkPoints2D
    # vtkPoints represents 3D points 
    # vtkPoints2D but no SetPoints2D: do we need to convert to 3D?
    points = vtkPoints()

    for i in range(0, len(tri_points)):
        # consider calling list() instead of tolist() to retain python type.
        # Otherwise, get nearest compatible Python type.

        points.InsertPoint(i, tri_points[i].tolist()) 
    ugrid = vtkUnstructuredGrid()

    ugrid.Allocate(100)

    for i in range(0, len(triangles)):
        ugrid.InsertNextCell(VTK_TRIANGLE,3, triangles[i].tolist()) 
    ugrid.SetPoints(points)

    # import vtk
    # print(dir(ugrid))
    # print(dir(vtk))
    # import vtk.vtkWriter
    # print(dir(vtk.vtkWriter))
    # print(dir(vtkUnstructuredGrid))
    # print(dir(vtkmodules.vtkCommonDataModel))
    # print(help(ugrid))
    

numpy_to_vtk()

