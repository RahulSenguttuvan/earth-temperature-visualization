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

class colorbar_param4:
    def __init__(self, title='Aerosol', title_col=[0,0,0], title_font_size=18, label_col=[0,0,0], pos=[0.02, 0.25], width=100, height=400, nlabels=6, font_size=14, title_offset=10):
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

class colorbar_param3:
    def __init__(self, title='Sea Temp', title_col=[0,0,0], title_font_size=18, label_col=[0,0,0], pos=[0.9, 0.1], width=100, height=400, nlabels=3, font_size=14, title_offset=10):
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
    def __init__(self, title='Land Temp', title_col=[0,0,0], title_font_size=18, label_col=[0,0,0], pos=[0.05, 0.1], width=100, height=400, nlabels=5, font_size=14, title_offset=10):
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

class colorbar_param1:
    def __init__(self, title='Radiation', title_col=[0,0,0], title_font_size=18, label_col=[0,0,0], pos=[0.9, 0.25], width=100, height=400, nlabels=3, font_size=14, title_offset=10):
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

    # define the color map for Shortwave Radiation
    colorMap1 = vtk.vtkColorTransferFunction()
    colorMap1.SetColorSpaceToRGB()
    colorMap1.AddRGBPoint(0, 0.15, 0.035, 0.62) # Blueish
    colorMap1.AddRGBPoint(213, 0.6, 0.89, 0.71) # Greenish
    colorMap1.AddRGBPoint(425, 1, 1, 1)  # White

    # color bar to display the color scale
    params1 = colorbar_param1()
    colorBar1 = colorbar(ctf=colorMap1,param=params1)
    colorBarActorRadiation = colorBar1.get()

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

    # define the color map for Aerosol Particle Radius
    colorMap4 = vtk.vtkColorTransferFunction()
    colorMap4.SetColorSpaceToRGB()
    colorMap4.AddRGBPoint(0, 0.101, 0.596, 0.313) 
    colorMap4.AddRGBPoint(20, 0.552, 0.807, 0.403)
    colorMap4.AddRGBPoint(40, 0.878, 0.949, 0.584) 
    colorMap4.AddRGBPoint(60, 0.996, 0.905, 0.588)
    colorMap4.AddRGBPoint(80, 0.976, 0.584, 0.333)
    colorMap4.AddRGBPoint(100, 0.847, 0.2, 0.156)

    # color bar to display the color scale
    params4 = colorbar_param4()
    colorBar4 = colorbar(ctf=colorMap4,param=params4)
    colorBarActorAerosol = colorBar4.get()

    monthLabelActor = vtk.vtkTextActor()
    monthLabelActor.SetInput("January")
    monthLabel = monthLabelActor.GetTextProperty()
    monthLabel.BoldOn()
    monthLabel.SetFontSize(26)
    monthLabel.SetColor(0,0,0)
    monthLabelActor.SetPosition(1100, 500)

    TextureList = ["Data/Land_Surface_Temperature/Day/color/Jan.jpg", "Data/Aerosol_Particle_Radius/Terra/color/Jan.jpg", "Data/Reflected_Shortwave_Radiation/color/Jan.jpg", "Data/Sea_Surface_Temperature/Day/color/Jan.jpg", "Data/Aerosol_Particle_Radius/Aqua/color/Jan.jpg"]
        
    # Load the elevation file
    geometry = "elevation_very_large.vti"
    ireader=vtk.vtkXMLImageDataReader()
    ireader.SetFileName(geometry)
    ireader.Update()

    # Set up the warp scalar
    warp=vtk.vtkWarpScalar()
    warp.SetInputConnection(ireader.GetOutputPort())
    warp.SetScaleFactor(200)
    warp.Update()

    transform = vtk.vtkTransform()
    transform.RotateWXYZ(180, 1, 0, 0)

    imapper=vtk.vtkDataSetMapper() 
    imapper.SetInputConnection(warp.GetOutputPort())
    imapper.SetScalarVisibility(False)

    # Load the image and Actors for Surface
    sreader_Land=vtk.vtkJPEGReader()
    sreader_Land.SetFileName(TextureList[0])

    texture_Land=vtk.vtkTexture()
    texture_Land.SetInputConnection(sreader_Land.GetOutputPort())

    iactor_Land=vtk.vtkActor()
    iactor_Land.SetMapper(imapper)
    iactor_Land.SetTexture(texture_Land)
    iactor_Land.SetUserTransform(transform)
    iactor_Land.SetPosition(0.0, 0.0, 0)

    sreader_Aqua=vtk.vtkJPEGReader()
    sreader_Aqua.SetFileName(TextureList[3])

    texture_Aqua=vtk.vtkTexture()
    texture_Aqua.SetInputConnection(sreader_Aqua.GetOutputPort())

    iactor_Aqua=vtk.vtkActor()
    iactor_Aqua.SetMapper(imapper)
    iactor_Aqua.SetTexture(texture_Aqua)
    iactor_Aqua.SetUserTransform(transform)
    iactor_Aqua.SetPosition(0.0, 0.0, 0)

    glyphActors = []
    x = [1,4]

    for i in x:

        # Load the JPG image
        imageReader=vtk.vtkJPEGReader()
        imageReader.SetFileName(TextureList[i])
        imageReader.Update()

        glyph_subset = vtk.vtkMaskPoints()
        glyph_subset.SetOnRatio(500)
        glyph_subset.SetInputConnection(imageReader.GetOutputPort())

        arrow_glyph_source = vtk.vtkArrowSource()
        arrow_glyph_source.SetTipLength(0)
        arrow_glyph_source.SetShaftRadius(0.4)
        # arrow_glyph_source.SetTipResolution(100)
        arrow_glyph_source.SetShaftResolution(10)

        # Create a glyph source and set its properties
        glyph = vtk.vtkGlyph3D()
        glyph.SetInputConnection(glyph_subset.GetOutputPort())
        glyph.SetSourceConnection(arrow_glyph_source.GetOutputPort())
        glyph.SetScaleFactor(0.05) # set size of glyph
        glyph.SetVectorModeToUseNormal()
        glyph.SetColorModeToColorByScalar()

        # Create a mapper and actor for the glyph
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(glyph.GetOutputPort())
    
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.SetOrigin(0,660,900)
        actor.SetScale(26000,36000,-5000)
        # actor.GetProperty().SetOpacity(0.1)

        glyphActors.append(actor)


    # Load the JPG image
    imageReader=vtk.vtkJPEGReader()
    imageReader.SetFileName(TextureList[2])
    imageReader.Update()

    glyph_subset = vtk.vtkMaskPoints()
    glyph_subset.SetOnRatio(500)
    glyph_subset.SetInputConnection(imageReader.GetOutputPort())

    arrow_glyph_source = vtk.vtkArrowSource()
    arrow_glyph_source.SetTipLength(0)
    arrow_glyph_source.SetShaftRadius(0.5)
    # arrow_glyph_source.SetTipResolution(100)
    arrow_glyph_source.SetShaftResolution(10)

    # Create a glyph source and set its properties
    glyph = vtk.vtkGlyph3D()
    glyph.SetInputConnection(glyph_subset.GetOutputPort())
    glyph.SetSourceConnection(arrow_glyph_source.GetOutputPort())
    glyph.SetScaleFactor(0.09) # set size of glyph
    glyph.SetVectorModeToUseNormal()
    glyph.SetColorModeToColorByScalar()

    # Create a mapper and actor for the glyph
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(glyph.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.SetOrigin(0,660,900)
    actor.SetScale(26000,33000,-5000)
    # actor.GetProperty().SetOpacity(0.1)

    glyphActors.append(actor)

    return [iactor_Land, iactor_Aqua, glyphActors, colorBarActorRadiation, colorBarActorLand, colorBarActorSea, colorBarActorAerosol, monthLabelActor]

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName('The Main Window')
        MainWindow.setWindowTitle('Glyphs')

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
        [self.landActor, self.aquaActor, self.glyphActors, self.colorBarActorRadiation, self.colorBarActorLand, self.colorBarActorSea, self.colorBarActorAerosol, self.monthLabelActor] = make()

        self.camera = vtk.vtkCamera()
        self.camera.SetPosition(-20320189.395117056, -51180285.12474119, 68436879.48824316)
        self.camera.SetFocalPoint(19967962.0, -9098651.0, 1939952.2792339325)
        self.camera.SetViewUp(0.13280725400613305, 0.7755140702442317, 0.6172034997766744)
        self.camera.SetClippingRange(52347229.45915045, 134012611.4728879)

        # Create the Renderer
        self.ren1 = vtk.vtkRenderer()
        self.ren1.AddActor(self.landActor)
        self.ren1.AddActor(self.glyphActors[0])
        self.ren1.AddActor(self.colorBarActorAerosol)
        self.ren1.AddActor(self.monthLabelActor)
        self.ren1.SetBackground(1, 1, 1)  # Set background to silver
        self.ren1.SetViewport(0.0, 0.5, 0.5, 1.0)
        self.ren1.SetActiveCamera(self.camera)
        self.ren1.ResetCamera()
        

        self.ren2 = vtk.vtkRenderer()
        self.ren2.AddActor(self.landActor)
        self.ren2.AddActor(self.glyphActors[2])
        self.ren2.AddActor(self.colorBarActorRadiation)
        self.ren2.SetBackground(1, 1, 1)  # Set background to silver
        self.ren2.SetViewport(0.5, 0.5, 1.0, 1.0)
        self.ren2.SetActiveCamera(self.camera)
        self.ren2.ResetCamera()
        

        self.ren3 = vtk.vtkRenderer()
        self.ren3.AddActor(self.aquaActor)
        self.ren3.AddActor(self.colorBarActorLand)
        self.ren3.AddActor(self.glyphActors[1])
        self.ren3.SetBackground(1, 1, 1)  # Set background to silver
        self.ren3.SetViewport(0.0, 0.0, 0.5, 0.5)
        self.ren3.SetActiveCamera(self.camera)
        self.ren3.ResetCamera()
        

        self.ren4 = vtk.vtkRenderer()
        self.ren4.AddActor(self.aquaActor)
        self.ren4.AddActor(self.glyphActors[2])
        self.ren4.AddActor(self.colorBarActorSea)
        self.ren4.SetBackground(1, 1, 1)  # Set background to silver
        self.ren4.SetViewport(0.5, 0.0, 1.0, 0.5)
        self.ren4.SetActiveCamera(self.camera)
        self.ren4.ResetCamera()
        self.ren1.GetActiveCamera().Zoom(1.6)
        
        self.ui.vtkWidget.GetRenderWindow().AddRenderer(self.ren1)
        self.ui.vtkWidget.GetRenderWindow().AddRenderer(self.ren2)
        self.ui.vtkWidget.GetRenderWindow().AddRenderer(self.ren3)
        self.ui.vtkWidget.GetRenderWindow().AddRenderer(self.ren4)
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

        landTexture = "Data/Land_Surface_Temperature/Day/color/" + self.landDayDataList[val]
        landAerosolTexture = "Data/Aerosol_Particle_Radius/Terra/color/" + self.landDayDataList[val]
        aquaAerosolTexture = "Data/Aerosol_Particle_Radius/Aqua/color/" + self.landDayDataList[val]
        reflectedWaveTexture = "Data/Reflected_Shortwave_Radiation/color/" + self.landDayDataList[val]
        seaTemperature = "Data/Sea_Surface_Temperature/Day/color/" + self.landDayDataList[val]

        ireader = vtk.vtkJPEGReader()
        texture=vtk.vtkTexture()
        ireader.SetFileName(landTexture)
        texture.SetInputConnection(ireader.GetOutputPort())
        self.landActor.SetTexture(texture)


        ireader = vtk.vtkJPEGReader()
        texture=vtk.vtkTexture()
        ireader.SetFileName(seaTemperature)
        texture.SetInputConnection(ireader.GetOutputPort())
        self.aquaActor.SetTexture(texture)


        imageReader=vtk.vtkJPEGReader()
        imageReader.SetFileName(landAerosolTexture)
        glyph_subset = vtk.vtkMaskPoints()
        glyph_subset.SetOnRatio(500)
        glyph_subset.SetInputConnection(imageReader.GetOutputPort())
        arrow_glyph_source = vtk.vtkArrowSource()
        arrow_glyph_source.SetTipLength(0)
        arrow_glyph_source.SetShaftRadius(0.4)
        # arrow_glyph_source.SetTipResolution(100)
        arrow_glyph_source.SetShaftResolution(10)
        glyph = vtk.vtkGlyph3D()
        glyph.SetInputConnection(glyph_subset.GetOutputPort())
        glyph.SetSourceConnection(arrow_glyph_source.GetOutputPort())
        glyph.SetScaleFactor(0.05) # set size of glyph
        glyph.SetVectorModeToUseNormal()
        glyph.SetColorModeToColorByScalar()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(glyph.GetOutputPort())
        self.glyphActors[0].SetMapper(mapper)
        self.glyphActors[0].SetOrigin(0,660,900)
        self.glyphActors[0].SetScale(26000,36000,-5000)


        imageReader=vtk.vtkJPEGReader()
        imageReader.SetFileName(reflectedWaveTexture)
        glyph_subset = vtk.vtkMaskPoints()
        glyph_subset.SetOnRatio(500)
        glyph_subset.SetInputConnection(imageReader.GetOutputPort())
        arrow_glyph_source = vtk.vtkArrowSource()
        arrow_glyph_source.SetTipLength(0)
        arrow_glyph_source.SetShaftRadius(0.5)
        # arrow_glyph_source.SetTipResolution(100)
        arrow_glyph_source.SetShaftResolution(10)
        glyph = vtk.vtkGlyph3D()
        glyph.SetInputConnection(glyph_subset.GetOutputPort())
        glyph.SetSourceConnection(arrow_glyph_source.GetOutputPort())
        glyph.SetScaleFactor(0.09) # set size of glyph
        glyph.SetVectorModeToUseNormal()
        glyph.SetColorModeToColorByScalar()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(glyph.GetOutputPort())
        self.glyphActors[2].SetMapper(mapper)
        self.glyphActors[2].SetOrigin(0,660,900)
        self.glyphActors[2].SetScale(26000,33000,-5000)


        imageReader=vtk.vtkJPEGReader()
        imageReader.SetFileName(aquaAerosolTexture)
        glyph_subset = vtk.vtkMaskPoints()
        glyph_subset.SetOnRatio(500)
        glyph_subset.SetInputConnection(imageReader.GetOutputPort())
        arrow_glyph_source = vtk.vtkArrowSource()
        arrow_glyph_source.SetTipLength(0)
        arrow_glyph_source.SetShaftRadius(0.4)
        # arrow_glyph_source.SetTipResolution(100)
        arrow_glyph_source.SetShaftResolution(10)
        glyph = vtk.vtkGlyph3D()
        glyph.SetInputConnection(glyph_subset.GetOutputPort())
        glyph.SetSourceConnection(arrow_glyph_source.GetOutputPort())
        glyph.SetScaleFactor(0.05) # set size of glyph
        glyph.SetVectorModeToUseNormal()
        glyph.SetColorModeToColorByScalar()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(glyph.GetOutputPort())
        self.glyphActors[1].SetMapper(mapper)
        self.glyphActors[1].SetOrigin(0,660,900)
        self.glyphActors[1].SetScale(26000,36000,-5000)
    
        self.ui.vtkWidget.GetRenderWindow().Render()

    def callback_func(self, caller, timer_event):
        global counter

        val = counter%len(self.landDayDataList)

        counter += 1

        self.monthLabelActor.SetInput(self.monthList[val])

        landTexture = "Data/Land_Surface_Temperature/Day/color/" + self.landDayDataList[val]
        landAerosolTexture = "Data/Aerosol_Particle_Radius/Terra/color/" + self.landDayDataList[val]
        aquaAerosolTexture = "Data/Aerosol_Particle_Radius/Aqua/color/" + self.landDayDataList[val]
        reflectedWaveTexture = "Data/Reflected_Shortwave_Radiation/color/" + self.landDayDataList[val]
        seaTemperature = "Data/Sea_Surface_Temperature/Day/color/" + self.landDayDataList[val]

        ireader = vtk.vtkJPEGReader()
        texture=vtk.vtkTexture()
        ireader.SetFileName(landTexture)
        texture.SetInputConnection(ireader.GetOutputPort())
        self.landActor.SetTexture(texture)


        ireader = vtk.vtkJPEGReader()
        texture=vtk.vtkTexture()
        ireader.SetFileName(seaTemperature)
        texture.SetInputConnection(ireader.GetOutputPort())
        self.aquaActor.SetTexture(texture)


        imageReader=vtk.vtkJPEGReader()
        imageReader.SetFileName(landAerosolTexture)
        glyph_subset = vtk.vtkMaskPoints()
        glyph_subset.SetOnRatio(500)
        glyph_subset.SetInputConnection(imageReader.GetOutputPort())
        arrow_glyph_source = vtk.vtkArrowSource()
        arrow_glyph_source.SetTipLength(0)
        arrow_glyph_source.SetShaftRadius(0.4)
        # arrow_glyph_source.SetTipResolution(100)
        arrow_glyph_source.SetShaftResolution(10)
        glyph = vtk.vtkGlyph3D()
        glyph.SetInputConnection(glyph_subset.GetOutputPort())
        glyph.SetSourceConnection(arrow_glyph_source.GetOutputPort())
        glyph.SetScaleFactor(0.05) # set size of glyph
        glyph.SetVectorModeToUseNormal()
        glyph.SetColorModeToColorByScalar()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(glyph.GetOutputPort())
        self.glyphActors[0].SetMapper(mapper)
        self.glyphActors[0].SetOrigin(0,660,900)
        self.glyphActors[0].SetScale(26000,36000,-5000)


        imageReader=vtk.vtkJPEGReader()
        imageReader.SetFileName(reflectedWaveTexture)
        glyph_subset = vtk.vtkMaskPoints()
        glyph_subset.SetOnRatio(500)
        glyph_subset.SetInputConnection(imageReader.GetOutputPort())
        arrow_glyph_source = vtk.vtkArrowSource()
        arrow_glyph_source.SetTipLength(0)
        arrow_glyph_source.SetShaftRadius(0.5)
        # arrow_glyph_source.SetTipResolution(100)
        arrow_glyph_source.SetShaftResolution(10)
        glyph = vtk.vtkGlyph3D()
        glyph.SetInputConnection(glyph_subset.GetOutputPort())
        glyph.SetSourceConnection(arrow_glyph_source.GetOutputPort())
        glyph.SetScaleFactor(0.09) # set size of glyph
        glyph.SetVectorModeToUseNormal()
        glyph.SetColorModeToColorByScalar()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(glyph.GetOutputPort())
        self.glyphActors[2].SetMapper(mapper)
        self.glyphActors[2].SetOrigin(0,660,900)
        self.glyphActors[2].SetScale(26000,33000,-5000)


        imageReader=vtk.vtkJPEGReader()
        imageReader.SetFileName(aquaAerosolTexture)
        glyph_subset = vtk.vtkMaskPoints()
        glyph_subset.SetOnRatio(500)
        glyph_subset.SetInputConnection(imageReader.GetOutputPort())
        arrow_glyph_source = vtk.vtkArrowSource()
        arrow_glyph_source.SetTipLength(0)
        arrow_glyph_source.SetShaftRadius(0.4)
        # arrow_glyph_source.SetTipResolution(100)
        arrow_glyph_source.SetShaftResolution(10)
        glyph = vtk.vtkGlyph3D()
        glyph.SetInputConnection(glyph_subset.GetOutputPort())
        glyph.SetSourceConnection(arrow_glyph_source.GetOutputPort())
        glyph.SetScaleFactor(0.05) # set size of glyph
        glyph.SetVectorModeToUseNormal()
        glyph.SetColorModeToColorByScalar()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(glyph.GetOutputPort())
        self.glyphActors[1].SetMapper(mapper)
        self.glyphActors[1].SetOrigin(0,660,900)
        self.glyphActors[1].SetScale(26000,36000,-5000)

        
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

    