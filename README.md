# VTK experiments for Fenics

## Setting up environment


## Building Fenics from `dolfinx/dev-env:current`:
Begin by pulling docker image:

`sudo docker pull dolfinx/dev-env:current`

Then run `build-dolfinx.sh`

## Issue with PETsc

Naming is now linux-gnu-real32-32/ in /usr/local/petsc

## Useful links:
[VTK Support for unstructured grids with global arrays. #3688](https://github.com/ornladios/ADIOS2/issues/3688pport for unstructured grids with global arrays)
[ADIOS2Wrappers for DOLFINx](https://github.com/jorgensd/adios4dolfinx/)
[Tutorial on meshes](https://jsdokken.com/dolfinx_docs/meshes.html)
[Jupyter notebook on meshes](https://github.com/jorgensd/dolfinx_docs/blob/main/meshes.ipynb)

[Dolfinx tutorial](https://jsdokken.com/dolfinx-tutorial/)
[ADIOS2 checkpointing I/O](https://hackmd.io/Zyz7pJWsQwCKM-t6Kr8OeQ)
[Logic for outputting mesh in vtk format in FEniCS](https://github.com/FEniCS/dolfinx/blob/main/python/dolfinx/plot.py)
# possibly not useful:
[numpy_to_vtk](https://pyscience.wordpress.com/2014/09/06/numpy-to-vtk-converting-your-numpy-arrays-to-vtk-arrays-and-files/)

If on getting to checkpointing: [Checkpointing](https://github.com/jorgensd/adios4dolfinx/issues/3) these are the two ways of doing it.

Final link:
[Grid format](https://dglaeser.github.io/gridformat/)



# VTK cell types are here:
# https://vtk.org/doc/nightly/html/vtkCellType_8h_source.html

# using the plot.py file for guidance
# https://github.com/FEniCS/dolfinx/blob/main/python/dolfinx/plot.py

# description of vtk file format
# https://examples.vtk.org/site/VTKFileFormats/

# mention of vtk in xdmf and why hdf is better
# https://www.kitware.com/vtk-hdf-reader/
# the implementation of the HDF5 reader
# https://gitlab.kitware.com/vtk/vtk/-/blob/master/IO/HDF/Testing/Cxx/TestHDFReader.cxx
# vtk xml to vtk hdf converter
# https://gitlab.kitware.com/danlipsa/vtkxml-to-vtkhdf

# xml formats : *.vtu

# https://discourse.vtk.org/

# from here:
# https://discourse.vtk.org/t/working-with-a-hdf-file-in-vtk/11233/7
# examples were listed
# https://examples.vtk.org/site/Python/

