# Real by default.a

export PYTHON_VERSION="3.10"

export PKG_CONFIG_PATH=/usr/local/dolfinx-real/lib/pkgconfig:$PKG_CONFIG_PATH \
    PETSC_ARCH=linux-gnu-real32-32 \
    PYTHONPATH=/usr/local/dolfinx-real/lib/python${PYTHON_VERSION}/dist-packages:$PYTHONPATH \
    LD_LIBRARY_PATH=/usr/local/dolfinx-real/lib:$LD_LIBRARY_PATH
