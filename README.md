# Julia  Volterra Touch  2022
==============================

## Functional Block Diagram

![alt-text](https://github.com/FracktalWorks/Julia2018ProDualABLTouchUI/blob/master/documentation/basic_blockdiagram.JPG?raw=true "Firmware Functional BLock Diagram")

* `MainWindow` is the object of `MainUiClass` class and this is the workhorse of the firmware where all the slots and event definitions are defined within this class. 
* `mainGUI_pro_dual_abl` is inherited by the `MainUiClass` class.
*  `mainGUI_pro_dual_abl` is the generated code from the `mainGUI_pro_dual_abl.ui` file which was made in Qt Designer and then converted into python code using PyQt5 UI code generator.
* `ThreadSanityCheck` checks for the availability of the server which runs on the Raspberry Pi and when available, establishes a connection with the MKS. It's initialized as `SanityCheck` in the `MainUiClass`.
*  Octoprint provides the web interface and `OctoprintAPI`, along with `REST API` and `Websockets` establishes a communication between the user and the server through HTTP and TCP protocols respectively. 
* `QtWebsocket` is the QT Thread that takes care of setting up slots and signals and it is initialized as `QtSocket` in `MainUiClass`.
* `Optopiclient` is the object of OctoprintAPI and is initialised as global in the `ThreadSanityCheck` class.
*  `OctoprintAPI` class has functions that handle the connection to the printer through a serial interface.
* `ThreadFileUpload` is the thread that has functions to upload the Gcode file to the server and is initialised as `uploadThread` in `MainUi_Class`.
* `Image` class creates a respective QR code that enables to open the web-interface on a mobile phone.



# To compile .ui to .py:
 pyuic4 .\mainGUI_pro_dual_abl.ui -o .\mainGUI_pro_dual_abl.py






