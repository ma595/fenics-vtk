import numpy as np

# https://pyscience.wordpress.com/2014/09/06/numpy-to-vtk-converting-your-numpy-arrays-to-vtk-arrays-and-files/
# https://discourse.vtk.org/t/how-to-include-a-time-series-in-a-vtkhdf-file/11430/13
## test.py for timeseries

# see:
# ./vtk-examples/src/Python/UnstructuredGrid/UGrid.py

    
def numpy_to_hdf5():
    """
    Defines a numpy array and outputs as VTK unstructured grid HDF5 format
    """
    
    import h5py

    tri_points = np.array([[0,0,0],[0,1,0],[1,0,0],[1,1,0]], dtype=np.float64)
    triangles = np.array([[0,1,3], [0,2,3]], dtype=np.int64)

    data = [tri_points, triangles]

    output_file = "test.hdf"
    
    with h5py.File(output_file, "w") as hdffile:
       # write support data
       whole_extent = None
       extent = None
       vtkhdf_group = hdffile.create_group("VTKHDF")
       vtkhdf_group.attrs.create("Version", [1, 0])
       number_of_pieces = 1   
       create_unstructuredgrid_hdf(tri_points, cells=triangles, number_of_pieces, vtkhdf_group)


    # num_of_connectivity_ids has size n (where num_of_connectivity[i] corresponds
    # to the size of the connectivity array for for partition i. 
    # number_of_connectivity_ids = [np_connectivity_size]
    # array of size n (corresponding to number of processes)
    # number_of_points = [np_points_size]
    # array of size n (corresponding to number of processes)
    # number_of_cells = [np_connectivity_size]


def create_unstructuredgrid_hdf(points, cells, number_of_pieces, vtkhdf_group):
    """
    Creates datasets needed for an unstructured grid: 
    Currently hardcoded triangular cells for the example above only.
    """
    tri_points = points
    number_of_cells = len(cells)
    cells_ravel = cells.ravel() # vtk hdf requires list of points
    np_points = tri_points
    np_points_size = len(tri_points)
    np_connectivity = cells_ravel
    np_connectivity_size = len(cells_ravel)
    np_offset = np.array([0, 3, 6]) # last entry corresponds to the length of the array https://vtk.org/doc/nightly/html/classvtkCellArray.html#details
    # np_offset_size = None
    np_types = np.array([5,5], dtype=np.ubyte)
    # np_types_size = 1 

    vtkhdf_group.attrs.create("Type", np.string_("UnstructuredGrid"))

    # connectivity_ids
    number_of_connectivity_ids = vtkhdf_group.create_dataset( "NumberOfConnectivityIds", (number_of_pieces,), np.int64)
    number_of_connectivity_ids[0] = np_connectivity_size 

    # points 
    number_of_points = vtkhdf_group.create_dataset( "NumberOfPoints", (number_of_pieces,), np.int64)
    number_of_points[0] = np_points_size

    # cells
    number_of_cells = vtkhdf_group.create_dataset( "NumberOfCells", (number_of_pieces,), np.int64)
    number_of_cells[0] = number_of_cells

    create_dataset("Points", np_points, vtkhdf_group)

    create_dataset("Connectivity", np_connectivity, vtkhdf_group)

    create_dataset("Offsets", np_offset, vtkhdf_group)

    # anp = vtk_to_numpy(data.GetCellTypesArray())
    # https://gitlab.kitware.com/vtk/vtk/-/blob/master/Documentation/docs/design_documents/VTKFileFormats.md
    # types
    create_dataset("Types", np_types, vtkhdf_group)
    
    field_data_group = vtkhdf_group.create_group("CellData")
#    field_data_group.attrs.create("scalars", np.string_("CTEST"))
    anp = np.array([1.0, 2.0])
    create_dataset("CTEST", anp, field_data_group)

    field_data_group = vtkhdf_group.create_group("PointData")
#    field_data_group.attrs.create("scalars", np.string_("PTEST"))
    anp = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    create_dataset("PTEST", anp, field_data_group)



def create_dataset(name, anp, group):
    """
    Create a HDF dataset 'name' inside 'group' from numpy array 'anp'.
    If number_of_pieces > 1 we create a dataset with size unlimited.
    """
    maxshape = anp.shape
    dset = group.create_dataset(name, anp.shape, anp.dtype, maxshape=maxshape)
    dset[0:] = anp
    return dset


numpy_to_hdf5()

