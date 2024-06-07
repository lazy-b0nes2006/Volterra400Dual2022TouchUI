from MainUIClass.config import getCalibrationPosition
from PyQt5 import QtGui
from MainUIClass.config import octopiclient
from MainUIClass.MainUIClasses.getFilesAndInfo import ThreadFileUpload

class calibrationPage:
    def __init__(self, MainUIObj):
        self.MainUIObj = MainUIObj

    def connect(self):
        self.MainUIObj.calibrateBackButton.pressed.connect(lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.MenuPage))
        self.MainUIObj.nozzleOffsetButton.pressed.connect(self.requestEEPROMProbeOffset)
        # the -ve sign is such that its converted to home offset and not just distance between nozzle and bed
        self.MainUIObj.nozzleOffsetSetButton.pressed.connect(
            lambda: self.setZProbeOffset(self.MainUIObj.nozzleOffsetDoubleSpinBox.value()))
        self.MainUIObj.nozzleOffsetBackButton.pressed.connect(lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.calibratePage))


        self.calibrationPosition = getCalibrationPosition(self.MainUIObj)

        self.MainUIObj.moveZMT1CaliberateButton.pressed.connect(lambda: octopiclient.jog(z=-0.025))
        self.MainUIObj.moveZPT1CaliberateButton.pressed.connect(lambda: octopiclient.jog(z=0.025))

        self.MainUIObj.calibrationWizardButton.clicked.connect(self.quickStep1)
        self.MainUIObj.quickStep1NextButton.clicked.connect(self.quickStep2)
        self.MainUIObj.quickStep2NextButton.clicked.connect(self.quickStep3)
        self.MainUIObj.quickStep3NextButton.clicked.connect(self.quickStep4)
        self.MainUIObj.quickStep4NextButton.clicked.connect(self.nozzleHeightStep1)
        self.MainUIObj.nozzleHeightStep1NextButton.clicked.connect(self.nozzleHeightStep1)
        self.MainUIObj.quickStep1CancelButton.pressed.connect(self.cancelStep)
        self.MainUIObj.quickStep2CancelButton.pressed.connect(self.cancelStep)
        self.MainUIObj.quickStep3CancelButton.pressed.connect(self.cancelStep)
        self.MainUIObj.quickStep4CancelButton.pressed.connect(self.cancelStep)
        self.MainUIObj.nozzleHeightStep1CancelButton.pressed.connect(self.cancelStep)
        
        self.MainUIObj.toolOffsetXSetButton.pressed.connect(self.setToolOffsetX)
        self.MainUIObj.toolOffsetYSetButton.pressed.connect(self.setToolOffsetY)
        self.MainUIObj.toolOffsetZSetButton.pressed.connect(self.setToolOffsetZ)
        self.MainUIObj.toolOffsetXYBackButton.pressed.connect(lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.calibratePage))
        self.MainUIObj.toolOffsetZBackButton.pressed.connect(lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.calibratePage))
        self.MainUIObj.toolOffsetXYButton.pressed.connect(self.updateToolOffsetXY)
        self.MainUIObj.toolOffsetZButton.pressed.connect(self.updateToolOffsetZ)

        self.MainUIObj.testPrintsButton.pressed.connect(lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.testPrintsPage1))
        self.MainUIObj.testPrintsNextButton.pressed.connect(lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.testPrintsPage2))
        self.MainUIObj.testPrintsBackButton.pressed.connect(lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.calibratePage))
        self.MainUIObj.testPrintsCancelButton.pressed.connect(lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.calibratePage))
        self.MainUIObj.dualCaliberationPrintButton.pressed.connect(
            lambda: self.testPrint(str(self.MainUIObj.testPrintsTool0SizeComboBox.currentText()).replace('.', ''),
                                   str(self.MainUIObj.testPrintsTool1SizeComboBox.currentText()).replace('.', ''), 'dualCalibration'))
        self.MainUIObj.bedLevelPrintButton.pressed.connect(
            lambda: self.testPrint(str(self.MainUIObj.testPrintsTool0SizeComboBox.currentText()).replace('.', ''),
                                   str(self.MainUIObj.testPrintsTool1SizeComboBox.currentText()).replace('.', ''), 'bedLevel'))
        self.MainUIObj.movementTestPrintButton.pressed.connect(
            lambda: self.testPrint(str(self.MainUIObj.testPrintsTool0SizeComboBox.currentText()).replace('.', ''),
                                   str(self.MainUIObj.testPrintsTool1SizeComboBox.currentText()).replace('.', ''), 'movementTest'))
        self.MainUIObj.singleNozzlePrintButton.pressed.connect(
            lambda: self.testPrint(str(self.MainUIObj.testPrintsTool0SizeComboBox.currentText()).replace('.', ''),
                                   str(self.MainUIObj.testPrintsTool1SizeComboBox.currentText()).replace('.', ''), 'dualTest'))
        self.MainUIObj.dualNozzlePrintButton.pressed.connect(
            lambda: self.testPrint(str(self.MainUIObj.testPrintsTool0SizeComboBox.currentText()).replace('.', ''),
                                   str(self.MainUIObj.testPrintsTool1SizeComboBox.currentText()).replace('.', ''), 'singleTest'))


    def getZHomeOffset(self, offset):
        '''
        Sets the spinbox value to have the value of the Z offset from the printer.
        the value is -ve so as to be more intuitive.
        :param offset:
        :return:
        '''
        self.MainUIObj.nozzleOffsetDoubleSpinBox.setValue(-float(offset))
        self.MainUIObj.nozzleHomeOffset = offset

    def setZHomeOffset(self, offset, setOffset=False):
        '''
        Sets the home offset after the calibration wizard is done, which is a callback to
        the response of M114 that is sent at the end of the Wizard in doneStep()
        :param offset: the value off the offset to set. is a str is coming from M114, and is float if coming from the nozzleOffsetPage
        :param setOffset: Boolean, is true if the function call is from the nozzleOffsetPage, else the current Z value sets the offset
        :return:

        #TODO can make this simpler, asset the offset value to string float to begin with instead of doing confitionals
        '''

        if self.MainUIObj.setHomeOffsetBool:
            octopiclient.gcode(command='M206 Z{}'.format(-float(offset)))
            self.MainUIObj.setHomeOffsetBool = False
            octopiclient.gcode(command='M500')
            # save in EEPROM
        if setOffset:    # When the offset needs to be set from spinbox value
            octopiclient.gcode(command='M206 Z{}'.format(-offset))
            octopiclient.gcode(command='M500')

    def setZToolOffset(self, offset, setOffset=False):
        '''
        Sets the home offset after the caliberation wizard is done, which is a callback to
        the response of M114 that is sent at the end of the Wizard in doneStep()
        :param offset: the value off the offset to set. is a str is coming from M114, and is float if coming from the nozzleOffsetPage
        :param setOffset: Boolean, is true if the function call is from the nozzleOFfsetPage
        :return:

        #TODO can make this simpler, asset the offset value to string float to begin with instead of doing confitionals
        '''
        self.currentZPosition = offset #gets the current z position, used to set new tool offsets.
        # clean this shit up.
        #fuck you past vijay for not cleaning this up
        if self.MainUIObj.setNewToolZOffsetFromCurrentZBool:
            newToolOffsetZ = float(self.toolOffsetZ) - float(self.currentZPosition)
            octopiclient.gcode(command='M218 T1 Z{}'.format(newToolOffsetZ))  # restore eeprom settings to get Z home offset, mesh bed leveling back
            self.MainUIObj.setNewToolZOffsetFromCurrentZBool =False
            octopiclient.gcode(command='M500')  # store eeprom settings to get Z home offset, mesh bed leveling back

    def showProbingFailed(self):
        self.MainUIObj.homePageInstance.tellAndReboot("Bed position is not calibrated. Please run calibration wizard after restart.")

    def updateEEPROMProbeOffset(self, offset):
        '''
        Sets the spinbox value to have the value of the Z offset from the printer.
        the value is -ve so as to be more intuitive.
        :param offset:
        :return:
        '''
        self.MainUIObj.nozzleOffsetDoubleSpinBox.setValue(float(offset))

    def setZProbeOffset(self, offset):
        '''
        Sets Z Probe offset from spinbox

        #TODO can make this simpler, asset the offset value to string float to begin with instead of doing confitionals
        '''

        octopiclient.gcode(command='M851 Z{}'.format(offset))
        octopiclient.gcode(command='M500')

    def requestEEPROMProbeOffset(self):
        '''
        Updates the value of M206 Z in the nozzle offset spinbox. Sends M503 so that the pritner returns the value as a websocket calback
        :return:
        '''
        octopiclient.gcode(command='M503')
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.nozzleOffsetPage)

    def nozzleOffset(self):
        '''
        Updates the value of M206 Z in the nozzle offset spinbox. Sends M503 so that the pritner returns the value as a websocket calback
        :return:
        '''
        octopiclient.gcode(command='M503')
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.nozzleOffsetPage)

    def updateToolOffsetXY(self):
        octopiclient.gcode(command='M503')
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.toolOffsetXYPage)

    def updateToolOffsetZ(self):
        octopiclient.gcode(command='M503')
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.toolOffsetZpage)

    def setToolOffsetX(self):
        octopiclient.gcode(command='M218 T1 X{}'.format(self.MainUIObj.toolOffsetXDoubleSpinBox.value()))  # restore eeprom settings to get Z home offset, mesh bed leveling back
        octopiclient.gcode(command='M500')

    def setToolOffsetY(self):
        octopiclient.gcode(command='M218 T1 Y{}'.format(self.MainUIObj.toolOffsetYDoubleSpinBox.value()))  # restore eeprom settings to get Z home offset, mesh bed leveling back
        octopiclient.gcode(command='M500')
        octopiclient.gcode(command='M500')

    def setToolOffsetZ(self):
        octopiclient.gcode(command='M218 T1 Z{}'.format(self.MainUIObj.toolOffsetZDoubleSpinBox.value()))  # restore eeprom settings to get Z home offset, mesh bed leveling back
        octopiclient.gcode(command='M500')

    def getToolOffset(self, M218Data):
        if float(M218Data[M218Data.index('X') + 1:].split(' ', 1)[0] ) > 0:
            self.toolOffsetZ = M218Data[M218Data.index('Z') + 1:].split(' ', 1)[0]
            self.toolOffsetX = M218Data[M218Data.index('X') + 1:].split(' ', 1)[0]
            self.toolOffsetY = M218Data[M218Data.index('Y') + 1:].split(' ', 1)[0]
            self.MainUIObj.toolOffsetXDoubleSpinBox.setValue(float(self.toolOffsetX))
            self.MainUIObj.toolOffsetYDoubleSpinBox.setValue(float(self.toolOffsetY))
            self.MainUIObj.toolOffsetZDoubleSpinBox.setValue(float(self.toolOffsetZ))

    def quickStep1(self):
        '''
        Shows welcome message.
        Homes to MAX
        goes to position where leveling screws can be opened
        :return:
        '''
        self.toolZOffsetCaliberationPageCount = 0
        octopiclient.gcode(command='M104 S200')
        octopiclient.gcode(command='M104 T1 S200')
        octopiclient.gcode(command='M211 S0')  # Disable software endstop
        octopiclient.gcode(command='T0')  # Set active tool to t0
        octopiclient.gcode(command='M503')  # makes sure internal value of Z offset and Tool offsets are stored before erasing
        octopiclient.gcode(command='M420 S0')  # Dissable mesh bed leveling for good measure
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.quickStep1Page)
        octopiclient.home(['x', 'y', 'z'])
        octopiclient.jog(x=40, y=40, absolute=True, speed=2000)

    def quickStep2(self):
        '''
        levels first position (RIGHT)
        :return:
        '''
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.quickStep2Page)
        octopiclient.jog(x=self.calibrationPosition['X1'], y=self.calibrationPosition['Y1'], absolute=True, speed=2000)
        octopiclient.jog(z=0, absolute=True, speed=1500)

    def quickStep3(self):
        '''
        levels second leveling position (LEFT)
        '''
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.quickStep3Page)
        octopiclient.jog(z=10, absolute=True, speed=1500)
        octopiclient.jog(x=self.calibrationPosition['X2'], y=self.calibrationPosition['Y2'], absolute=True, speed=2000)
        octopiclient.jog(z=0, absolute=True, speed=1500)

    def quickStep4(self):
        '''
        levels third leveling position  (BACK)
        :return:
        '''
        # sent twice for some reason
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.quickStep4Page)
        octopiclient.jog(z=10, absolute=True, speed=1500)
        octopiclient.jog(x=self.calibrationPosition['X3'], y=self.calibrationPosition['Y3'], absolute=True, speed=2000)
        octopiclient.jog(z=0, absolute=True, speed=1500)

    # def quickStep5(self):
    #     '''
    #     Nozzle Z offset calc
    #     '''
    #     self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.quickStep5Page)
    #     octopiclient.jog(z=15, absolute=True, speed=1500)
    #     octopiclient.gcode(command='M272 S')

    def nozzleHeightStep1(self):
        if self.toolZOffsetCaliberationPageCount == 0 :
            self.toolZOffsetLabel.setText("Move the bed up or down to the First Nozzle , testing height using paper")
            self.stackedWidget.setCurrentWidget(self.nozzleHeightStep1Page)
            octopiclient.jog(z=10, absolute=True, speed=1500)
            octopiclient.jog(x=self.calibrationPosition['X4'], y=self.calibrationPosition['Y4'], absolute=True, speed=2000)
            octopiclient.jog(z=1, absolute=True, speed=1500)
            self.toolZOffsetCaliberationPageCount = 1
        elif self.toolZOffsetCaliberationPageCount == 1:
            self.toolZOffsetLabel.setText("Move the bed up or down to the Second Nozzle , testing height using paper")
            octopiclient.gcode(command='G92 Z0')#set the current Z position to zero
            octopiclient.jog(z=1, absolute=True, speed=1500)
            octopiclient.gcode(command='T1')
            self.toolZOffsetCaliberationPageCount = 2
        else:
            self.doneStep()

    def doneStep(self):
        '''
        Exits leveling
        :return:
        '''
        self.MainUIObj.setNewToolZOffsetFromCurrentZBool = True
        octopiclient.gcode(command='M114')
        octopiclient.jog(z=4, absolute=True, speed=1500)
        octopiclient.gcode(command='T0')
        octopiclient.gcode(command='M211 S1')  # Disable software endstop
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.calibratePage)
        octopiclient.home(['x', 'y', 'z'])
        octopiclient.gcode(command='M104 S0')
        octopiclient.gcode(command='M104 T1 S0')
        octopiclient.gcode(command='M500')  # store eeprom settings to get Z home offset, mesh bed leveling back

    def cancelStep(self):
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.calibratePage)
        octopiclient.home(['x', 'y', 'z'])
        octopiclient.gcode(command='M104 S0')
        octopiclient.gcode(command='M104 T1 S0')


    def testPrint(self,tool0Diameter,tool1Diameter,gcode):
        '''
        Prints a test print
        :param tool0Diameter: Diameter of tool 0 nozzle.04,06 or 08
        :param tool1Diameter: Diameter of tool 1 nozzle.40,06 or 08
        :param gcode: type of gcode to print, dual nozzle calibration, bed leveling, movement or samaple prints in
        single and dual. bedLevel, dualCalibration, movementTest, dualTest, singleTest
        :return:
        '''
        try:
            if gcode is 'bedLevel':
                self.printFromPath('gcode/' + tool0Diameter + '_BedLeveling.gcode', True)
            elif gcode is 'dualCalibration':
                self.printFromPath(
                    'gcode/' + tool0Diameter + '_' + tool1Diameter + '_dual_extruder_calibration_Volterra.gcode',
                    True)
            elif gcode is 'movementTest':
                self.printFromPath('gcode/movementTest.gcode', True)
            elif gcode is 'dualTest':
                self.printFromPath(
                    'gcode/' + tool0Diameter + '_' + tool1Diameter + '_Fracktal_logo_Volterra.gcode',
                    True)
            elif gcode is 'singleTest':
                self.printFromPath('gcode/' + tool0Diameter + '_Fracktal_logo_Volterra.gcode',True)

            else:
                print("gcode not found")
        except Exception as e:
            print("Eror:" + e)
    
    def printFromPath(self,path,prnt=True):
        '''
        Transfers a file from a specific to octoprint's watched folder so that it gets automatically detected by Octoprint.
        Warning: If the file is read-only, octoprint API for reading the file crashes.
        '''

        self.MainUIObj.uploadThread = ThreadFileUpload(path, prnt=prnt)
        self.MainUIObj.uploadThread.start()
        if prnt:
            self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.homePage)
    