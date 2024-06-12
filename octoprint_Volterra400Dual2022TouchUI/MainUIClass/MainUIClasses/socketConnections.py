class socketConnections:
    def __init__(self, MainUIObj):
        self.MainUIObj = MainUIObj

    def connect(self):
        #--Dual Caliberation Addition--
        self.MainUIObj.QtSocket.set_z_tool_offset_signal.connect(self.MainUIObj.calibrationPageInstance.setZToolOffset)
        self.MainUIObj.QtSocket.z_probe_offset_signal.connect(self.MainUIObj.calibrationPageInstance.updateEEPROMProbeOffset)
        self.MainUIObj.QtSocket.temperatures_signal.connect(self.MainUIObj.printerStatusInstance.updateTemperature)
        self.MainUIObj.QtSocket.status_signal.connect(self.MainUIObj.printerStatusInstance.updateStatus)
        self.MainUIObj.QtSocket.print_status_signal.connect(self.MainUIObj.printerStatusInstance.updatePrintStatus)
        self.MainUIObj.QtSocket.update_started_signal.connect(self.MainUIObj.softwareUpdatePageInstance.softwareUpdateProgress)
        self.MainUIObj.QtSocket.update_log_signal.connect(self.MainUIObj.softwareUpdatePageInstance.softwareUpdateProgressLog)
        self.MainUIObj.QtSocket.update_log_result_signal.connect(self.MainUIObj.softwareUpdatePageInstance.softwareUpdateResult)
        self.MainUIObj.QtSocket.update_failed_signal.connect(self.MainUIObj.softwareUpdatePageInstance.updateFailed)
        self.MainUIObj.QtSocket.connected_signal.connect(self.MainUIObj.onServerConnected)
        self.MainUIObj.QtSocket.filament_sensor_triggered_signal.connect(self.MainUIObj.filamentSensorInstance.filamentSensorHandler)
        self.MainUIObj.QtSocket.firmware_updater_signal.connect(self.MainUIObj.firmwareUpdatePageInstance.firmwareUpdateHandler)
        #self.MainUIObj.QtSocket.z_home_offset_signal.connect(self.MainUIObj.calibrationPageInstance.getZHomeOffset)  Deprecated, uses probe offset to set initial height instead
        self.MainUIObj.QtSocket.active_extruder_signal.connect(self.MainUIObj.activeExtruderInstance.setActiveExtruder)


        
