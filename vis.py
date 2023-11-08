# inspired by https://discourse.vtk.org/t/working-with-a-hdf-file-in-vtk/11233/5

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkRenderingCore import (

    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)
import vtk


def render_data(file_name):
    colors = vtkNamedColors()
    reader = vtk.vtkHDFReader()
    reader.SetFileName(file_name)
    reader.Update()

    outDS = reader.GetOutput()
    # outDS.GetPointData().SetScalars(outDS.GetPointData().GetArray("PNGImage"))
    print(outDS.GetPointData().GetArray("PTEST"))

    outDS.GetPointData().SetScalars(outDS.GetPointData().GetArray("PTEST"))


    print(dir(vtk))
    imageXY = vtk.vtkExtractUnstructuredGrid()
    #imageXY.SetInputConnection(reader.GetOutputPort())
    #imageXY.SetVOI(0, 2999, 0, 2999, 0, 0)

    imageXY.Update()
#
#    XYSliceActor = vtk.vtkImageActor()
#    XYSliceActor.SetPosition(-1500, -1500, -500)
#    XYSliceActor.GetMapper().SetInputConnection(imageXY.GetOutputPort())
#
#    ip = vtk.vtkImageProperty()
#    ip.SetColorWindow(255)
#    ip.SetColorLevel(128)
#    ip.SetAmbient(0.0)
#    ip.SetDiffuse(1.0)
#    ip.SetOpacity(1.0)
#    ip.SetInterpolationTypeToLinear()
#
#    XYSliceActor.SetProperty(ip)
#    XYSliceActor.Update()
#
#    colors = vtk.vtkNamedColors()
#    # Create the Renderer
#    renderer = vtk.vtkRenderer()
#    renderer.AddActor(XYSliceActor)
#    renderer.ResetCamera()
#    renderer.SetBackground(colors.GetColor3d('Silver'))
#
#    # Create the RendererWindow
#    renderer_window = vtk.vtkRenderWindow()
#    renderer_window.AddRenderer(renderer)
#    renderer_window.SetWindowName('ReadImageData')
#
#    # Create the RendererWindowInteractor and display the VTKHDF file
#    interactor = vtk.vtkRenderWindowInteractor()
#    interactor.SetRenderWindow(renderer_window)
#    interactor.Initialize()
#    interactor.Start()
    return []

if __name__ == '__main__':

    output_file = './test.hdf'
    img = render_data(output_file)
    #plt.imshow(img)
    #plt.show()
    # render_data(output_file)

# outDS.GetPointData().SetScalars(outDS.GetPointData().GetArray("test"))

# print(dir(outDS))

# print(outDS.GetCellData())
# print(outDS.GetPointData())
# print(outDS.GetPoints())
# print(outDS.GetCells())
