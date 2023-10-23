#! /bin/bash
# The following ARGS are used in the DOLFINx layer.
# They are safe defaults.
# CMake build type for DOLFINx C++ build. See CMake documentation.
export DOLFINX_CMAKE_BUILD_TYPE="RelWithDebInfo"
# Extra CMake C++ compiler flags for DOLFINx C++ build.
export DOLFINX_CMAKE_CXX_FLAGS=-O2

set -u

# The dolfinx-onbuild container expects to have folders basix/ ufl/
# ffcx/ and dolfinx/ mounted/shared at /src.
#cd basix && cmake -G Ninja -DCMAKE_BUILD_TYPE=${DOLFINX_CMAKE_BUILD_TYPE} -DCMAKE_CXX_FLAGS=${DOLFINX_CMAKE_CXX_FLAGS} -B build-dir -S ./cpp && \
#    cmake --build build-dir && \
#    cmake --install build-dir && \
#    python3 -m pip install ./python && \
#    cd ../ufl && pip3 install --no-cache-dir . && \
#    cd ../ffcx && pip3 install --no-cache-dir . && \
#    cd ../ && pip3 install --no-cache-dir ipython

export PETSC_DIR=/usr/local/petsc 
export SLEPC_DIR=/usr/local/slepc
export PYTHON_VERSION=3.10
cd dolfinx && \
    mkdir -p build-real && \
    cd build-real && \
    PETSC_DIR=/usr/local/petsc/ PETSC_ARCH=linux-gnu-real32-32 cmake -G Ninja -DCMAKE_INSTALL_PREFIX=/usr/local/dolfinx-real -DCMAKE_BUILD_TYPE=${DOLFINX_CMAKE_BUILD_TYPE} -DCMAKE_CXX_FLAGS=${DOLFINX_CMAKE_CXX_FLAGS} ../cpp && \
    ninja install && \
    cd ../python && \
    CXXFLAGS=${DOLFINX_CMAKE_CXX_FLAGS} PETSC_ARCH=linux-gnu-real32-32 pip3 install -v --target /usr/local/dolfinx-real/lib/python${PYTHON_VERSION}/dist-packages --no-dependencies --no-cache-dir . && \
    git clean -fdx && \
    cd ../ && \
    mkdir -p build-complex && \
    cd build-complex && \
    PETSC_ARCH=linux-gnu-complex32-32 cmake -G Ninja -DCMAKE_INSTALL_PREFIX=/usr/local/dolfinx-complex -DCMAKE_BUILD_TYPE=${DOLFINX_CMAKE_BUILD_TYPE} -DCMAKE_CXX_FLAGS=${DOLFIN_CMAKE_CXX_FLAGS} ../cpp && \
    ninja install && \
    . /usr/local/dolfinx-complex/lib/dolfinx/dolfinx.conf && \
    cd ../python && \
    CXXFLAGS=${DOLFINX_CMAKE_CXX_FLAGS} PETSC_ARCH=linux-gnu-complex32-32 pip3 install -v --target /usr/local/dolfinx-complex/lib/python${PYTHON_VERSION}/dist-packages --no-dependencies --no-cache-dir .

# Real by default.
export PKG_CONFIG_PATH=/usr/local/dolfinx-real/lib/pkgconfig:$PKG_CONFIG_PATH \
    PETSC_ARCH=linux-gnu-real-32 \
    PYTHONPATH=/usr/local/dolfinx-real/lib/python${PYTHON_VERSION}/dist-packages:$PYTHONPATH \
    LD_LIBRARY_PATH=/usr/local/dolfinx-real/lib:$LD_LIBRARY_PATH
