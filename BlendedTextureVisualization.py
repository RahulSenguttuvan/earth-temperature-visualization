#!/usr/bin/env python

# CS 530 - Assignment 1 - Task 3
# Name: Piyush Jaiswal
# PUID: 0033660375


# import libraries
import vtk
import matplotlib.pyplot as plt
from vtk.util import numpy_support
import numpy as np
import argparse
import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QSlider, QGridLayout, QLabel, QPushButton, QTextEdit
import PyQt5.QtCore as QtCore
from PyQt5.QtCore import Qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

# Counter to keep a track of screenshots
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



def make():

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

    monthLabelActor = vtk.vtkTextActor()
    monthLabelActor.SetInput("January")
    monthLabel = monthLabelActor.GetTextProperty()
    monthLabel.BoldOn()
    monthLabel.SetFontSize(26)
    monthLabel.SetColor(0,0,0)
    monthLabelActor.SetPosition(1100, 1000)

    TextureList = ["Data/Land_Surface_Temperature/Day/color/Jan.jpg",  "Data/Land_Surface_Temperature/Night/color/Jan.jpg", "Data/Sea_Surface_Temperature/Day/color/Jan.jpg"]
        
    # Load the elevation file
    geometry = "elevation_sphere_medium.vtp"
    elevationReader=vtk.vtkXMLPolyDataReader()
    elevationReader.SetFileName(geometry)
    elevationReader.Update()

    # Set up the warp scalar
    warp=vtk.vtkWarpScalar()
    warp.SetInputConnection(elevationReader.GetOutputPort())
    warp.SetScaleFactor(50)
    warp.Update()

    elevationMapper=vtk.vtkDataSetMapper() 
    elevationMapper.SetInputConnection(warp.GetOutputPort())
    # elevationMapper.SetScalarVisibility(False)

    elevationActor = vtk.vtkActor()
    elevationActor.SetMapper(elevationMapper)

    # Blended Land and Sea Day Temperature
    sreader_Land_Day=vtk.vtkJPEGReader()
    sreader_Land_Day.SetFileName(TextureList[0])
    sreader_Land_Day.Update()

    sreader_Sea_Day=vtk.vtkJPEGReader()
    sreader_Sea_Day.SetFileName(TextureList[2])
    sreader_Sea_Day.Update()

    blend1 = vtk.vtkImageBlend()
    blend1.AddInputData(sreader_Land_Day.GetOutput())
    blend1.AddInputData(sreader_Sea_Day.GetOutput())
    blend1.SetOpacity(0, 0.5)
    blend1.SetOpacity(1, 0.5)
    blend1.Update()

    texture1=vtk.vtkTexture()
    texture1.SetInputData(blend1.GetOutput())

    textureMapper1=vtk.vtkDataSetMapper() 
    textureMapper1.SetInputConnection(warp.GetOutputPort())
    textureMapper1.SetScalarVisibility(False)

    textureActor1=vtk.vtkActor()
    textureActor1.SetMapper(textureMapper1)
    textureActor1.SetTexture(texture1)

    # Blended Land and Sea Night Temperature
    sreader_Land_Night=vtk.vtkJPEGReader()
    sreader_Land_Night.SetFileName(TextureList[1])
    sreader_Land_Night.Update()

    sreader_Sea_Night=vtk.vtkJPEGReader()
    sreader_Sea_Night.SetFileName(TextureList[2])
    sreader_Sea_Night.Update()

    blend2 = vtk.vtkImageBlend()
    blend2.AddInputData(sreader_Land_Night.GetOutput())
    blend2.AddInputData(sreader_Sea_Night.GetOutput())
    blend2.SetOpacity(0, 0.5)
    blend2.SetOpacity(1, 0.5)
    blend2.Update()

    texture2=vtk.vtkTexture()
    texture2.SetInputData(blend2.GetOutput())

    textureMapper2=vtk.vtkDataSetMapper() 
    textureMapper2.SetInputConnection(warp.GetOutputPort())
    textureMapper2.SetScalarVisibility(False)

    textureActor2=vtk.vtkActor()
    textureActor2.SetMapper(textureMapper2)
    textureActor2.SetTexture(texture2)


    return [elevationActor, textureActor1, textureActor2, colorBarActorLand, colorBarActorSea, monthLabelActor]

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName('The Main Window')
        MainWindow.setWindowTitle('Blended Textures')

        self.centralWidget = QWidget(MainWindow)
        self.gridlayout = QGridLayout(self.centralWidget)
        self.vtkWidget = QVTKRenderWindowInteractor(self.centralWidget)

        # Sliders
        self.slider_scale_factor = QSlider()

        # Button
        self.button_widget = QPushButton()
        self.button_widget.setToolTip('Animate')
        self.button_widget.setText('Animate')

        #Positioning
        self.gridlayout.addWidget(self.vtkWidget, 0, 0, 4, 4)
        self.gridlayout.addWidget(QLabel("Variations Over Time"), 4, 0, 1, 1)
        self.gridlayout.addWidget(self.slider_scale_factor, 4, 1, 1, 1)
        self.gridlayout.addWidget(self.button_widget, 5, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralWidget)

class viewEarth(QMainWindow):

    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.landDayDataList = ["Jan.jpg", "Feb.jpg", "March.jpg", "April.jpg", "May.jpg", "June.jpg", "July.jpg", "Aug.jpg", "Sep.jpg", "Oct.jpg", "Nov.jpg", "Dec.jpg"]
        self.monthList = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        
        # Source
        [self.elevationActor, self.textureActor1, self.textureActor2, self.colorBarActorLand, self.colorBarActorSea, self.monthLabelActor] = make()

        self.camera = vtk.vtkCamera()
        self.camera.SetPosition(-42568611.66855305, -1932492.8152799588, 5581270.639632868)
        self.camera.SetFocalPoint(-28877.0, 16082.5, -62250.5)
        self.camera.SetViewUp(0.1168078045852825, 0.2406383262234357, 0.9635606533790958)
        self.camera.SetClippingRange(27727917.634025127, 62230140.58728261)

        # Create the Renderer
        self.ren1 = vtk.vtkRenderer()
        self.ren1.AddActor(self.elevationActor)
        self.ren1.AddActor(self.textureActor1)
        self.ren1.AddActor(self.colorBarActorLand)
        self.ren1.AddActor(self.monthLabelActor)
        self.ren1.SetBackground(1, 1, 1)  # Set background to silver
        self.ren1.SetViewport(0.0, 0.0, 0.5, 1.0)
        self.ren1.SetActiveCamera(self.camera)
        self.ren1.ResetCamera()
        

        self.ren2 = vtk.vtkRenderer()
        self.ren2.AddActor(self.elevationActor)
        self.ren2.AddActor(self.textureActor2)
        self.ren2.AddActor(self.colorBarActorSea)
        self.ren2.SetBackground(1, 1, 1)  # Set background to silver
        self.ren2.SetViewport(0.5, 0.0, 1.0, 1.0)
        self.ren2.SetActiveCamera(self.camera)
        self.ren2.ResetCamera()
        self.ren2.GetActiveCamera().Zoom(1.2)
        
        self.ui.vtkWidget.GetRenderWindow().AddRenderer(self.ren1)
        self.ui.vtkWidget.GetRenderWindow().AddRenderer(self.ren2)
        self.iren = self.ui.vtkWidget.GetRenderWindow().GetInteractor()

        self.iren.AddObserver("KeyPressEvent", self.key_pressed_callback)

        def slider_setup(slider, val, bounds, interv):
            slider.setOrientation(QtCore.Qt.Horizontal)
            slider.setValue(int(val))
            slider.setTracking(False)
            slider.setTickInterval(interv)
            slider.setTickPosition(QSlider.TicksAbove)
            slider.setRange(bounds[0], bounds[1])
        
        slider_setup(self.ui.slider_scale_factor, 0, [0, 11], 1)
    
    # Fucnction to change the images 
    def scalefactor_callback(self, val):
        self.scaleFactor = val
        
        self.monthLabelActor.SetInput(self.monthList[val])

        landTemperatureDay = "Data/Land_Surface_Temperature/Day/color/" + self.landDayDataList[val]
        landTemperatureNight = "Data/Land_Surface_Temperature/Night/color/" + self.landDayDataList[val]
        seaTemperature = "Data/Sea_Surface_Temperature/Day/color/" + self.landDayDataList[val]

        ireader1=vtk.vtkJPEGReader()
        ireader2=vtk.vtkJPEGReader()
        texture=vtk.vtkTexture()
        blend = vtk.vtkImageBlend()
        ireader1.SetFileName(landTemperatureDay)
        ireader1.Update()
        ireader2.SetFileName(seaTemperature)
        ireader2.Update()
        blend.AddInputData(ireader1.GetOutput())
        blend.AddInputData(ireader2.GetOutput())
        blend.SetOpacity(0, 0.5)
        blend.SetOpacity(1, 0.5)
        blend.Update()
        texture.SetInputData(blend.GetOutput())
        self.textureActor1.SetTexture(texture)

        ireader1=vtk.vtkJPEGReader()
        ireader2=vtk.vtkJPEGReader()
        texture=vtk.vtkTexture()
        blend = vtk.vtkImageBlend()
        ireader1.SetFileName(landTemperatureNight)
        ireader1.Update()
        ireader2.SetFileName(seaTemperature)
        ireader2.Update()
        blend.AddInputData(ireader1.GetOutput())
        blend.AddInputData(ireader2.GetOutput())
        blend.SetOpacity(0, 0.5)
        blend.SetOpacity(1, 0.5)
        blend.Update()
        texture.SetInputData(blend.GetOutput())
        self.textureActor2.SetTexture(texture)

    
        self.ui.vtkWidget.GetRenderWindow().Render()

    def callback_func(self, caller, timer_event):
        global counter

        val = counter%len(self.landDayDataList)

        counter += 1

        self.monthLabelActor.SetInput(self.monthList[val])

        landTemperatureDay = "Data/Land_Surface_Temperature/Day/color/" + self.landDayDataList[val]
        landTemperatureNight = "Data/Land_Surface_Temperature/Night/color/" + self.landDayDataList[val]
        seaTemperature = "Data/Sea_Surface_Temperature/Day/color/" + self.landDayDataList[val]

        ireader1=vtk.vtkJPEGReader()
        ireader2=vtk.vtkJPEGReader()
        texture=vtk.vtkTexture()
        blend = vtk.vtkImageBlend()
        ireader1.SetFileName(landTemperatureDay)
        ireader1.Update()
        ireader2.SetFileName(seaTemperature)
        ireader2.Update()
        blend.AddInputData(ireader1.GetOutput())
        blend.AddInputData(ireader2.GetOutput())
        blend.SetOpacity(0, 0.5)
        blend.SetOpacity(1, 0.5)
        blend.Update()
        texture.SetInputData(blend.GetOutput())
        self.textureActor1.SetTexture(texture)

        ireader1=vtk.vtkJPEGReader()
        ireader2=vtk.vtkJPEGReader()
        texture=vtk.vtkTexture()
        blend = vtk.vtkImageBlend()
        ireader1.SetFileName(landTemperatureNight)
        ireader1.Update()
        ireader2.SetFileName(seaTemperature)
        ireader2.Update()
        blend.AddInputData(ireader1.GetOutput())
        blend.AddInputData(ireader2.GetOutput())
        blend.SetOpacity(0, 0.5)
        blend.SetOpacity(1, 0.5)
        blend.Update()
        texture.SetInputData(blend.GetOutput())
        self.textureActor2.SetTexture(texture)

        
        time.sleep(0.5)

        self.ui.vtkWidget.GetRenderWindow().Render()

    # Define the button press event callback function
    def pushbutton_animate(self):
        global animation_running
        global timer_id

        if not animation_running:
            # Start the animation if it's not already running
            animation_running = True
            timer_id = window.iren.CreateRepeatingTimer(500)
            window.iren.AddObserver("TimerEvent", window.callback_func)
        else:
            # Stop the animation if it's currently running
            animation_running = False
            if timer_id is not None:
                window.iren.DestroyTimer(timer_id)

    def key_pressed_callback(self, obj, event):
        global args
        # ---------------------------------------------------------------
        # Attach actions to specific keys
        # ---------------------------------------------------------------
        key = obj.GetKeySym()
        if key == "c":
            print(self.ren2.GetActiveCamera().GetPosition())
            print(self.ren1.GetActiveCamera().GetFocalPoint())
            print(self.ren1.GetActiveCamera().GetViewUp())
            print(self.ren1.GetActiveCamera().GetClippingRange())
        
        elif key == "q":
            sys.exit()

   


if __name__ == "__main__":
    # Parsing the API
    parser=argparse.ArgumentParser(description='Project - ')

    args=parser.parse_args()

    app = QApplication(sys.argv)
    window = viewEarth()
    window.ui.vtkWidget.GetRenderWindow().SetSize(800, 800)
    window.show()
    window.setWindowState(Qt.WindowMaximized)  # Maximize the window
    window.iren.Initialize() # Need this line to actually show
                             # the render inside Qt

    window.ui.slider_scale_factor.valueChanged.connect(window.scalefactor_callback)
    window.ui.button_widget.clicked.connect(window.pushbutton_animate)

    sys.exit(app.exec_())

    