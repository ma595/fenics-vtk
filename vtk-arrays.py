from dolfinx import cpp as _cpp
from dolfinx import fem, mesh
import numpy as np

from vtkmodules.vtkCommonDataModel import (
    VTK_TRIANGLE,
    VTK_VERTEX,
    vtkUnstructuredGrid
)

import vtkmodules

# based on:
## https://pyscience.wordpress.com/2014/09/06/numpy-to-vtk-converting-your-numpy-arrays-to-vtk-arrays-and-files/
## ./vtk-examples/src/Python/UnstructuredGrid/UGrid.py


def numpy_to_vtk():

    tri_points = np.array([[0,0,0],[0,1,0],[1,0,0],[1,1,0]], dtype=np.float64)
    triangles = np.array([[0,1,3], [0,2,3]], dtype=np.int64)

    from vtkmodules.vtkCommonCore import vtkPoints, vtkPoints2D
    # vtkPoints represents 3D points - vtkPoints2D but no SetPoints2D - do we need to convert to 3D?
    points = vtkPoints()


    for i in range(0, len(tri_points)):
        points.InsertPoint(i, tri_points[i].tolist()) # convert to python list - consider calling list() instead to retain python type. Otherwise, get nearest compatible Python type.

    ugrid = vtkUnstructuredGrid()
    # print(dir("ugrid "), ugrid)
    ugrid.Allocate(100)

    for i in range(0, len(triangles)):
        ugrid.InsertNextCell(VTK_TRIANGLE,3, triangles[i].tolist()) # convert to python list

    # print(dir(ugrid))
    ugrid.SetPoints(points)

    

    ##print(dir(ugrid))

    print(dir(vtkmodules))

    # import vtkmodules
    import vtk
    # print(dir(vtk))
    # import vtk.vtkWriter
    # print(dir(vtk.vtkWriter))

    # print(dir(vtkUnstructuredGrid))
    # print(dir(vtkmodules.vtkCommonDataModel))

    # print(help(ugrid))

    import vtk.io
    print(vtk.io)
    

numpy_to_vtk()

# help(ugrid)

# creating an imagehdf from https://discourse.vtk.org/t/working-with-a-hdf-file-in-vtk/11233/9
def create_vtkhdf_dataset(output_file, image_dir, image_height, image_width, num_images, pixel_size_xy, pixel_size_z):

    with h5py.File(output_file,'w') as hdffile:

        # write support data
        vtkhdf_group = hdffile.create_group("VTKHDF")
        vtkhdf_group.attrs.create("Version", [1, 0])

        vtkhdf_group.attrs.create("Type", np.string_("ImageData"))
        whole_extent = (0, image_width-1, 0, image_height-1, 0, num_images-1)
        vtkhdf_group.attrs.create("WholeExtent", whole_extent)

        vtkhdf_group.attrs.create("Origin", (0.0, 0.0, 0.0))
        vtkhdf_group.attrs.create("Spacing", (pixel_size_xy, pixel_size_xy, pixel_size_z))
        vtkhdf_group.attrs.create("Direction", (1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0))

        # create the pointdata group and the dataset inside it
        field_data_group = vtkhdf_group.create_group("PointData")
        field_data_group.attrs.create('Scalars', np.string_("PNGImage"))
        dset = field_data_group.create_dataset('PNGImage',dtype=np.uint8,shape=(num_images,image_height,image_width))

# from vtk.util import numpy_support 
# this does not work for complex arrays
# not sure how this works for points and triangles defined as above.
# help(numpy_support.numpy_to_vtk)
