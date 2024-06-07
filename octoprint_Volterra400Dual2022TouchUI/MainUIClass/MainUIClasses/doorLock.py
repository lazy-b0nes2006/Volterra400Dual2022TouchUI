from MainUIClass.MainUIClass_def import octopiclient
import dialog
from PyQt5 import QtGui
from MainUIClass.config import _fromUtf8

class doorLock:
    def __init__(self, MainUIObj):
        self.MainUIObj = MainUIObj
    
    def doorLock(self):
        '''
        function that toggles locking and unlocking the front door
        :return:
        '''
        octopiclient.overrideDoorLock()

    def doorLockMsg(self, data):
        if "msg" not in data:
            return

        msg = data["msg"]

        if self.MainUIObj.dialog_doorlock:
            self.MainUIObj.dialog_doorlock.close()
            self.MainUIObj.dialog_doorlock = None

        if msg is not None:
            self.MainUIObj.dialog_doorlock = dialog.dialog(self.MainUIObj, msg, icon="exclamation-mark.png")
            if self.MainUIObj.dialog_doorlock.exec_() == QtGui.QMessageBox.Ok:
                self.MainUIObj.dialog_doorlock = None
                return

    def doorLockHandler(self, data):
        door_lock_disabled = False
        door_lock = False
        # door_sensor = False
        # door_lock_override = False

        if 'door_lock' in data:
            door_lock_disabled = data["door_lock"] == "disabled"
            door_lock = data["door_lock"] == 1
        # if 'door_sensor' in data:
        #     door_sensor = data["door_sensor"] == 1
        # if 'door_lock_override' in data:
        #     door_lock_override = data["door_lock_override"] == 1

        # if self.MainUIObj.dialog_doorlock:
        #     self.MainUIObj.dialog_doorlock.close()
        #     self.MainUIObj.dialog_doorlock = None

        self.MainUIObj.doorLockButton.setVisible(not door_lock_disabled)
        if not door_lock_disabled:
            # self.doorLockButton.setChecked(not door_lock)
            self.MainUIObj.doorLockButton.setText('Lock Door' if not door_lock else 'Unlock Door')

            icon = 'doorLock' if not door_lock else 'doorUnlock'
            self.MainUIObj.doorLockButton.setIcon(QtGui.QIcon(_fromUtf8("templates/img/" + icon + ".png")))
        else:
            return
