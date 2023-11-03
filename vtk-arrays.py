import numpy as np

# https://pyscience.wordpress.com/2014/09/06/numpy-to-vtk-converting-your-numpy-arrays-to-vtk-arrays-and-files/

# see:
# ./vtk-examples/src/Python/UnstructuredGrid/UGrid.py

def numpy_to_vtk():

    from vtkmodules.vtkCommonDataModel import (
        VTK_TRIANGLE,
        VTK_VERTEX,
        vtkUnstructuredGrid
    )

    import vtkmodules
    print(dir(vtkmodules))

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
    
def numpy_to_hdf5():
    # Questions: 
    # If we define points - should they be defined in 3D?
    # assuming a single process.
    import h5py

    tri_points = np.array([[0,0,0],[0,1,0],[1,0,0],[1,1,0]], dtype=np.float64)
    triangles = np.array([[0,1,3], [0,2,3]], dtype=np.int64)

    data = [tri_points, triangles]

    output_file = "test.hdf5"
    
    with h5py.File(output_file, "w") as hdffile:
       # write support data
       whole_extent = None
       extent = None
       vtkhdf_group = hdffile.create_group("VTKHDF")
       vtkhdf_group.attrs.create("Version", [1, 0])
       (points, points_size, connectivity, connectivity_size, offset, offset_size, types, types_size, number_of_connectivity_ids, number_of_points, number_of_cells) = (None, None, None, None, None, None, None, None, None, None, None)

       number_of_pieces = 1   
       (points, points_size, connectivity, connectivity_size, offset, offset_size, types, types_size, number_of_connectivity_ids, number_of_points, number_of_cells) = create_support_unstructuredgrid(data, number_of_pieces, vtkhdf_group)


def create_support_unstructuredgrid(data, number_of_pieces, vtkhdf_group):
    """
    Creates datasets needed for an unstructured grid: NumberOfConnectivityIds,
    NumberOfPoints, NumberOfCells (needed for showing pieces),
    Points, Connectivity, Offsets, Types
    """
    tri_points = data[0]
    triangles = data[1].ravel() # not sure whether this should be ravelled, only way to make offsets make sense. 

    print(tri_points)
    np_points = tri_points
    np_points_size = len(tri_points)
    np_connectivity = triangles
    print("connectivitiy ", np_connectivity)
    np_connectivity_size = len(triangles)
    print(np_connectivity)
    np_offset = np.array([0, 3, 6]) # last entry corresponds to the length of the array https://vtk.org/doc/nightly/html/classvtkCellArray.html#details
    print("np_offset shape", np_offset.shape)
    print("offsets", np_offset)
    print("offsets dtype", np_offset.dtype)
    np_offset_size = None
    np_types = None
    np_types_size = 1 
    # num_of_connectivity_ids has size n (where num_of_connectivity[i] corresponds
    # to the size of the connectivity array for for partition i. 
    number_of_connectivity_ids = [np_connectivity_size]
    # array of size n (corresponding to number of processes)
    number_of_points = [np_points_size]
    # array of size n (corresponding to number of processes)

    number_of_cells = [np_connectivity_size]

    vtkhdf_group.attrs.create("Type", np.string_("UnstructuredGrid"))
    cells = triangles

    number_of_connectivity_ids = vtkhdf_group.create_dataset(
        "NumberOfConnectivityIds", (number_of_pieces,), np.int64)
    # number_of_connectivity_ids[0] = cells.GetNumberOfConnectivityIds()
    number_of_connectivity_ids[0] = 2 # ?
    number_of_points = vtkhdf_group.create_dataset(
        "NumberOfPoints", (number_of_pieces,), np.int64)
    number_of_points[0] = np_points_size
    number_of_cells = vtkhdf_group.create_dataset(
        "NumberOfCells", (number_of_pieces,), np.int64)
    # number_of_cells[0] = cells.GetNumberOfCells()
    number_of_cells[0] = 2

    # anp = vtk_to_numpy(data.GetPoints().GetData
    anp = np_points
    points = create_dataset("Points", anp, vtkhdf_group)
    points_size = anp.shape[0]

    # anp = vtk_to_numpy(cells.GetConnectivityArray())
    anp = np_connectivity # ravelled connectivity 
    connectivity = create_dataset("Connectivity", anp, vtkhdf_group)
    connectivity_size = anp.shape[0]

    # anp = vtk_to_numpy(cells.GetOffsetsArray())
    anp = np_offset
    offset = create_dataset("Offsets", anp, vtkhdf_group)
    offset_size = anp.shape[0]
    print(anp.shape[0])

    # anp = vtk_to_numpy(data.GetCellTypesArray())
    # https://gitlab.kitware.com/vtk/vtk/-/blob/master/Documentation/docs/design_documents/VTKFileFormats.md
    # this needs to be unsigned char
    anp = np.array([5, 5], dtype=np.ubyte)
    types = create_dataset("Types", anp, vtkhdf_group)
    types_size = anp.shape[0]
    return (points, points_size, connectivity, connectivity_size,
            offset, offset_size, types, types_size,
            number_of_connectivity_ids, number_of_points, number_of_cells)


def create_dataset(name, anp, group):
    """
    Create a HDF dataset 'name' inside 'group' from numpy array 'anp'.
    If number_of_pieces > 1 we create a dataset with size unlimited.
    """
    shape = anp.shape
    maxshape = shape
    dset = group.create_dataset(name, shape, anp.dtype, maxshape=maxshape)
    dset[0:] = anp
    return dset



# def dolfinx_to_hdf5():
#     from dolfinx import cpp as _cpp
#     from dolfinx import fem, mesh

numpy_to_hdf5()

