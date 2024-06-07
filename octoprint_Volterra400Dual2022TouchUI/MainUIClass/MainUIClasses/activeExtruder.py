from MainUIClass.MainUIClass_def import octopiclient
from MainUIClass.config import _fromUtf8
from PyQt5 import QtGui

class activeExtruder:
    def __init__(self, MainUIObj):
        self.MainUIObj = MainUIObj

    def connect(self):
        self.MainUIObj.toolToggleMotionButton.clicked.connect(self.selectToolMotion)
        self.MainUIObj.toolToggleChangeFilamentButton.clicked.connect(self.selectToolChangeFilament)
        self.MainUIObj.toolToggleTemperatureButton.clicked.connect(self.selectToolTemperature)


    def selectToolChangeFilament(self):
        '''
        Selects the tool whose temperature needs to be changed. It accordingly changes the button text. it also updates the status of the other toggle buttons
        '''

        if self.toolToggleChangeFilamentButton.isChecked():
            self.setActiveExtruder(1)
            octopiclient.selectTool(1)
        else:
            self.setActiveExtruder(0)
            octopiclient.selectTool(0)

    def selectToolMotion(self):
        '''
        Selects the tool whose temperature needs to be changed. It accordingly changes the button text. it also updates the status of the other toggle buttons
        '''

        if self.toolToggleMotionButton.isChecked():
            self.setActiveExtruder(1)
            octopiclient.selectTool(1)

        else:
            self.setActiveExtruder(0)
            octopiclient.selectTool(0)

    def selectToolTemperature(self):
        '''
        Selects the tool whose temperature needs to be changed. It accordingly changes the button text.it also updates the status of the other toggle buttons
        '''
        # self.toolToggleTemperatureButton.setText(
        #     "1") if self.toolToggleTemperatureButton.isChecked() else self.toolToggleTemperatureButton.setText("0")
        if self.toolToggleTemperatureButton.isChecked():
            print ("extruder 1 Temperature")
            self.toolTempSpinBox.setProperty("value", float(self.tool1TargetTemperature.text()))
        else:
            print ("extruder 0 Temperature")
            self.toolTempSpinBox.setProperty("value", float(self.tool0TargetTemperature.text()))

    def setActiveExtruder(self, activeNozzle):
        activeNozzle = int(activeNozzle)
        if activeNozzle == 0:
            self.tool0Label.setPixmap(QtGui.QPixmap(_fromUtf8("templates/img/activeNozzle.png")))
            self.tool1Label.setPixmap(QtGui.QPixmap(_fromUtf8("templates/img/Nozzle.png")))
            self.toolToggleChangeFilamentButton.setChecked(False)
            # self.toolToggleChangeFilamentButton.setText("0")
            self.toolToggleMotionButton.setChecked(False)
            self.toolToggleMotionButton.setText("0")
            self.activeExtruder = 0
        elif activeNozzle == 1:
            self.tool0Label.setPixmap(QtGui.QPixmap(_fromUtf8("templates/img/Nozzle.png")))
            self.tool1Label.setPixmap(QtGui.QPixmap(_fromUtf8("templates/img/activeNozzle.png")))
            self.toolToggleChangeFilamentButton.setChecked(True)
            # self.toolToggleChangeFilamentButton.setText("1")
            self.toolToggleMotionButton.setChecked(True)
            self.toolToggleMotionButton.setText("1")
            self.activeExtruder = 1

            # set button states
            # set octoprint if mismatch
