from mpi4py import MPI
import dolfinx
from dolfinx import mesh
import numpy as np

comm = MPI.COMM_WORLD
world_rank = comm.Get_rank()
world_size = comm.Get_size()

# with shared facet see:
# https://jsdokken.com/dolfinx_docs/meshes.html

ghost_mode = dolfinx.mesh.GhostMode.none
# ghost_mode = dolfinx.mesh.GhostMode.shared_facet
domain = mesh.create_unit_square(MPI.COMM_WORLD, 1, 1, mesh.CellType.triangle, ghost_mode=ghost_mode)

print("Num triangles on process ", world_rank, " : ", domain.topology.index_map(2).size_local)
print("Num nodes on process", world_rank, " : ", domain.topology.index_map(0).size_local)

# 
domain.topology.create_connectivity(2,0)
print("Connectivity on process ", world_rank, domain.topology.connectivity(2,0))
domain.topology.create_connectivity(0,0)
print("Nodes on process ", world_rank, domain.topology.connectivity(0,0))

# how to get triangles per process
# and how to get x 


indices_1d = domain.topology.index_map(0).size_local
print("Geometry on process ", world_rank, "\n", domain.geometry.x)
print("Local to global indices ", world_rank, "\n", print((domain.geometry.index_map().local_to_global([0,1,2]))))

#geom_map = domain.geometry.index_map().local_to_global(0)
top_map = domain.topology.index_map(2).local_to_global([0])
print(top_map)
#print(geom_map([0]))

