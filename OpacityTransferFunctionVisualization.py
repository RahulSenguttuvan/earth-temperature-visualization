import vtk
import sys
import numpy as np
import argparse
import time
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QSlider, QGridLayout, QLabel, QPushButton
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import Qt

frame_counter = 0
counter = 0
timer_id = None
animation_running = False

class colorbar_param3:
    def __init__(self, title='Sea Temp', title_col=[0,0,0], title_font_size=18, label_col=[0,0,0], pos=[0.88, 0.3], width=100, height=600, nlabels=3, font_size=14, title_offset=10):
        self.title=title
        self.title_col=title_col
        self.label_col=label_col
        self.pos=pos
        self.width=width
        self.height=height
        self.nlabels=nlabels
        self.font_size=font_size
        self.title_offset=title_offset
        self.title_font_size=title_font_size

class colorbar_param2:
    def __init__(self, title='Land Temp', title_col=[0,0,0], title_font_size=18, label_col=[0,0,0], pos=[0.07, 0.3], width=100, height=600, nlabels=5, font_size=14, title_offset=10):
        self.title=title
        self.title_col=title_col
        self.label_col=label_col
        self.pos=pos
        self.width=width
        self.height=height
        self.nlabels=nlabels
        self.font_size=font_size
        self.title_offset=title_offset
        self.title_font_size=title_font_size

class colorbar:
    def __init__(self, ctf, param, is_float=True):
        # Create a color bar
        self.scalar_bar = vtk.vtkScalarBarActor()
        # size and relative position
        self.scalar_bar.SetLookupTable(ctf)
        self.scalar_bar.SetPosition(param.pos[0], param.pos[1])
        self.scalar_bar.SetMaximumWidthInPixels(param.width)
        self.scalar_bar.SetMaximumHeightInPixels(param.height)
        # title properties
        self.scalar_bar.SetTitle(param.title)
        self.scalar_bar.GetTitleTextProperty().SetColor(param.title_col[0], param.title_col[1],  param.title_col[2])
        self.scalar_bar.SetVerticalTitleSeparation(param.title_offset)
        self.scalar_bar.GetTitleTextProperty().ShadowOff()
        self.scalar_bar.GetTitleTextProperty().SetFontSize(param.title_font_size)
        self.scalar_bar.GetTitleTextProperty().BoldOn()
        self.scalar_bar.GetLabelTextProperty().SetFontSize(param.font_size)
        self.scalar_bar.GetLabelTextProperty().BoldOn()
        self.scalar_bar.UnconstrainedFontSizeOn()
        # label properties
        self.scalar_bar.SetNumberOfLabels(param.nlabels)
        self.scalar_bar.SetTextPad(4)
        self.scalar_bar.DrawTickLabelsOn()
        if is_float:
            format='%0.2f'
        else:
            format='%0.0f'
        self.scalar_bar.SetLabelFormat(format)
        self.scalar_bar.GetLabelTextProperty().SetColor(param.label_col[0],
                                                   param.label_col[1],
                                                   param.label_col[2])
        self.scalar_bar.GetLabelTextProperty().SetFontSize(param.font_size)
        self.scalar_bar.GetLabelTextProperty().BoldOff()
        self.scalar_bar.GetLabelTextProperty().ShadowOff()

    def get(self):
        return self.scalar_bar

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Set Name for Qt UI 
        MainWindow.setObjectName('The Main Window')
        MainWindow.setWindowTitle('View Earth Visualization - Task 3')
    
        # Qt central widget 
        self.centralWidget = QWidget(MainWindow)
        # Grid for organizing widgets
        self.gridlayout = QGridLayout(self.centralWidget)

        # Add central widget to vtkRenderWindow
        self.vtkWidget = QVTKRenderWindowInteractor(self.centralWidget)
        
        # Sliders
        self.slider_scale_factor = QSlider()
        # Button
        self.button_widget = QPushButton()
        self.button_widget.setToolTip('Animate')
        self.button_widget.setText('Animate')

        # We are now going to position our widgets inside our
        # grid layout. The top left corner is (0,0)
        # Here we specify that our vtkWidget is anchored to the top
        # left corner and spans 3 rows and 4 columns.
        self.gridlayout.addWidget(self.vtkWidget, 0, 0, 4, 4)
        self.gridlayout.addWidget(QLabel("Variations Over Time"), 4, 0, 1, 1)
        self.gridlayout.addWidget(self.slider_scale_factor, 4, 1, 1, 1)
        self.gridlayout.addWidget(self.button_widget, 5, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)

class PyQtDemo(QMainWindow):

    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    # define the color map for Land Surface Temperature
        colorMap2 = vtk.vtkColorTransferFunction()
        colorMap2.SetColorSpaceToRGB()
        colorMap2.AddRGBPoint(-25, 0.66, 0.93, 0.96) 
        colorMap2.AddRGBPoint(-7.5, 0.2, 0.31, 0.8) 
        colorMap2.AddRGBPoint(10, 0.78, 0.004, 0.61)  
        colorMap2.AddRGBPoint(27.5, 0.92, 0.37, 0) 
        colorMap2.AddRGBPoint(45, 0.97, 0.93, 0.43) 

        # color bar to display the color scale
        params2 = colorbar_param2()
        colorBar2 = colorbar(ctf=colorMap2,param=params2)
        colorBarActorLand = colorBar2.get()

    # define the color map for Sea Surface Temperature
        colorMap3 = vtk.vtkColorTransferFunction()
        colorMap3.SetColorSpaceToRGB()
        colorMap3.AddRGBPoint(-2, 0.066, 0.094, 0.356) 
        colorMap3.AddRGBPoint(16.5, 0.62, 0.403, 0.592)
        colorMap3.AddRGBPoint(35, 0.988, 0.929, 0.784)

        # color bar to display the color scale
        params3 = colorbar_param3()
        colorBar3 = colorbar(ctf=colorMap3,param=params3)
        colorBarActorSea = colorBar3.get()


        self.landDayDataList = ["Jan.jpg", "Feb.jpg", "March.jpg", "April.jpg", "May.jpg", "June.jpg", "July.jpg", "Aug.jpg", "Sep.jpg", "Oct.jpg", "Nov.jpg", "Dec.jpg"]
        sphereTextureList = ["Data/Land_Surface_Temperature/Day/color/Jan.jpg", "Data/Sea_Surface_Temperature/Day/color/Jan.jpg", "Data/Land_Surface_Temperature/Night/color/Jan.jpg",  "Data/Sea_Surface_Temperature/Day/color/Jan.jpg"]
        self.sphereActorList = []
        self.monthList = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

        self.monthLabelActor = vtk.vtkTextActor()
        self.monthLabelActor.SetInput("January")
        
        monthLabel = self.monthLabelActor.GetTextProperty()
        monthLabel.BoldOn()
        monthLabel.SetFontSize(26)
        monthLabel.SetColor(0,0,0)
        
        self.monthLabelActor.SetPosition(1100, 1000)

        landDayActorList = []
        landDayActorList1 = []
    
        earthGeometry = vtk.vtkXMLPolyDataReader()
        earthGeometry.SetFileName("elevation_sphere_medium.vtp")
        earthGeometry.Update()

        self.warp = vtk.vtkWarpScalar()
        self.warp.SetInputConnection(earthGeometry.GetOutputPort())
        self.warp.SetScaleFactor(0)
        self.warp.Update()  

        warp_mapper=vtk.vtkDataSetMapper() 
        warp_mapper.SetInputConnection(self.warp.GetOutputPort())
        warp_mapper.ScalarVisibilityOff()

        for textures in sphereTextureList:
            # imagePath = landDayPath+month
            ireader = vtk.vtkJPEGReader()
            ireader.SetFileName(textures)
            
            texture=vtk.vtkTexture()
            texture.SetInputConnection(ireader.GetOutputPort())

            self.actor = vtk.vtkActor()
            self.actor.SetMapper(warp_mapper)
            self.actor.SetTexture(texture)
            self.actor.GetProperty()

            self.sphereActorList.append(self.actor)
    
        
        camera = vtk.vtkCamera()
        camera.SetPosition(-40619276.35291144, -16119065.07604465, 9215334.294560548)
        camera.SetFocalPoint(14.174999999813735, 0.0, 0.0)
        camera.SetViewUp(0.1562419143405155, 0.16319912585869903, 0.9741429615421793)
        camera.SetClippingRange(24602909.066174723, 70019462.68981642)

        self.render_window_1 = vtk.vtkRenderer()
        self.render_window_1.SetViewport(0.0, 0.0, 0.5, 1.0)
        self.render_window_1.SetActiveCamera(camera)
        self.sphereActorList[0].SetScale(1.05,1.05,1.05)
        self.sphereActorList[0].GetProperty().SetOpacity(0.5)
        self.render_window_1.AddActor(self.sphereActorList[0])
        self.render_window_1.AddActor(self.sphereActorList[1])
        self.render_window_1.AddActor(colorBarActorLand)
        self.render_window_1.AddActor(self.monthLabelActor)
        self.render_window_1.SetBackground(vtk.vtkNamedColors().GetColor3d("White"))
        self.render_window_1.ResetCamera()
        
        
        self.render_window_2 = vtk.vtkRenderer()
        self.render_window_2.SetViewport(0.5, 0.0, 1.0, 1.0)
        self.render_window_2.SetActiveCamera(camera)
        self.sphereActorList[2].SetScale(1.05,1.05,1.05)
        self.sphereActorList[2].GetProperty().SetOpacity(0.5)
        self.render_window_2.AddActor(self.sphereActorList[2])
        self.render_window_2.AddActor(self.sphereActorList[3])
        self.render_window_2.AddActor(colorBarActorSea)
        self.render_window_2.SetBackground(vtk.vtkNamedColors().GetColor3d("white"))
        self.render_window_2.ResetCamera()
        self.render_window_2.GetActiveCamera().Zoom(1.15)


        self.ui.vtkWidget.GetRenderWindow().AddRenderer(self.render_window_1)
        self.ui.vtkWidget.GetRenderWindow().AddRenderer(self.render_window_2)
    
        self.interactor = self.ui.vtkWidget.GetRenderWindow().GetInteractor()
        # Setting up widgets

        def slider_setup(slider, val, bounds, interv):
            slider.setOrientation(QtCore.Qt.Horizontal)
            slider.setValue(int(val))
            slider.setTracking(False)
            slider.setTickInterval(interv)
            slider.setTickPosition(QSlider.TicksAbove)
            slider.setRange(bounds[0], bounds[1])
        
        slider_setup(self.ui.slider_scale_factor, 0, [0, 11], 1)


    # Fucnction to change the scale 
    def scalefactor_callback(self, val):
        self.scaleFactor = val

        self.monthLabelActor.SetInput(self.monthList[val])
        
        landDayTexture = "Data/Land_Surface_Temperature/Day/color/" + self.landDayDataList[val]
        landNightTexture = "Data/Land_Surface_Temperature/Night/color/" + self.landDayDataList[val]
        seaTemperature = "Data/Sea_Surface_Temperature/Day/color/" + self.landDayDataList[val]

        ireader = vtk.vtkJPEGReader()
        texture=vtk.vtkTexture()
        
        ireader.SetFileName(landDayTexture)
        texture.SetInputConnection(ireader.GetOutputPort())

        self.sphereActorList[0].SetTexture(texture)

        ireader = vtk.vtkJPEGReader()
        texture=vtk.vtkTexture()
        ireader.SetFileName(seaTemperature)
        texture.SetInputConnection(ireader.GetOutputPort())

        self.sphereActorList[1].SetTexture(texture)
        self.sphereActorList[3].SetTexture(texture)


        ireader = vtk.vtkJPEGReader()
        texture=vtk.vtkTexture()
        ireader.SetFileName(landNightTexture)
        texture.SetInputConnection(ireader.GetOutputPort())

        self.sphereActorList[2].SetTexture(texture)
        self.ui.vtkWidget.GetRenderWindow().Render()


    def callback_func(self, caller, timer_event):
        global counter

        val = counter%len(self.landDayDataList)
        print(val)
        self.monthLabelActor.SetInput(self.monthList[val])
        counter += 1

        landDayTexture = "Data/Land_Surface_Temperature/Day/color/" + self.landDayDataList[val]
        landNightTexture = "Data/Land_Surface_Temperature/Night/color/" + self.landDayDataList[val]
        seaTemperature = "Data/Sea_Surface_Temperature/Day/color/" + self.landDayDataList[val]

        ireader = vtk.vtkJPEGReader()
        texture=vtk.vtkTexture()
        
        ireader.SetFileName(landDayTexture)
        texture.SetInputConnection(ireader.GetOutputPort())

        self.sphereActorList[0].SetTexture(texture)

        ireader = vtk.vtkJPEGReader()
        texture=vtk.vtkTexture()
        ireader.SetFileName(seaTemperature)
        texture.SetInputConnection(ireader.GetOutputPort())

        self.sphereActorList[1].SetTexture(texture)
        self.sphereActorList[3].SetTexture(texture)


        ireader = vtk.vtkJPEGReader()
        texture=vtk.vtkTexture()
        ireader.SetFileName(landNightTexture)
        texture.SetInputConnection(ireader.GetOutputPort())

        self.sphereActorList[2].SetTexture(texture)

        time.sleep(0.5)
        self.ui.vtkWidget.GetRenderWindow().Render()

    # Define the button press event callback function
    def pushbutton_animate(self):
        global animation_running
        global timer_id

        if not animation_running:
            # Start the animation if it's not already running
            animation_running = True
            timer_id = window.interactor.CreateRepeatingTimer(500)
            window.interactor.AddObserver("TimerEvent", window.callback_func)
        else:
            # Stop the animation if it's currently running
            animation_running = False
            if timer_id is not None:
                window.interactor.DestroyTimer(timer_id)
        
    def print_camera_settings(self):
        # global renderer
        # ---------------------------------------------------------------
        # Print out the current settings of the camera
        # ---------------------------------------------------------------
        camera = self.render_window_1.GetActiveCamera()
        print("Camera settings:")
        print("  * position:        %s" % (camera.GetPosition(),))
        print("  * focal point:     %s" % (camera.GetFocalPoint(),))
        print("  * up vector:       %s" % (camera.GetViewUp(),))
        print("  * clipping range:  %s" % (camera.GetClippingRange(),))

    
    # Helper function used to add key press for functionality
    def key_pressed_callback(self,obj, event):
        global args
        # ---------------------------------------------------------------
        # Attach actions to specific keys
        # ---------------------------------------------------------------
        key = obj.GetKeySym()
        if key == "h":
            print("Commands:\n 's': save frame\n 'q': quit the program")
        elif key == "s":
            self.save_frame()
        elif key == "c":
            self.print_camera_settings()
        elif key == "q":
            sys.exit()

    # Function to save a frame. 
    def save_frame(self):
        global frame_counter
        # ---------------------------------------------------------------
        # Save current contents of render window to PNG file
        # ---------------------------------------------------------------
        file_name = "View_Earth" + str(frame_counter).zfill(5) + ".png"
        image = vtk.vtkWindowToImageFilter()
        image.SetInput(self.ui.vtkWidget.GetRenderWindow())
        png_writer = vtk.vtkPNGWriter()
        png_writer.SetInputConnection(image.GetOutputPort())
        png_writer.SetFileName(file_name)
        self.ui.vtkWidget.GetRenderWindow().Render()
        png_writer.Write()
        frame_counter += 1

    # def clippingPlaneX_callback(self, val):
    #     window.ui.log.clear()
    #     window.ui.log.insertPlainText('Set Clipping Plane X to {}\n'.format(val))
    #     self.clipX = val
    #     self.planeX.SetOrigin(val, 0, 0)
    #     self.ui.vtkWidget.GetRenderWindow().Render()


if __name__=="__main__":
    global args

    parser = argparse.ArgumentParser(description='Assignment 1 Task 3')

    args = parser.parse_args()
    
    # Class required to manage widget based GUI applications 
    app = QApplication(sys.argv)
    # PyQtDemo class called to construct Qt interface
    window = PyQtDemo()
    window.ui.vtkWidget.GetRenderWindow().SetSize(1024, 768)
    
    # Get output 
    window.show()
    # Maximize the window
    window.setWindowState(Qt.WindowMaximized)  
    window.interactor.AddObserver("KeyPressEvent", window.key_pressed_callback)
    # Need this line to actually show - Interactor called 
    window.interactor.Initialize()
    
    # When scale factor changes, render UI
    window.ui.slider_scale_factor.valueChanged.connect(window.scalefactor_callback)
    window.ui.button_widget.clicked.connect(window.pushbutton_animate)

    sys.exit(app.exec_())
