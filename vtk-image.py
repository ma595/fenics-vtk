
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
