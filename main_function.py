from PyQt5.QtCore import Qt, QThread, QTimer, QRect, QMetaObject, QCoreApplication, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QSizePolicy, QMessageBox
from PyQt5.QtGui import QImage, QColor
from pyqtgraph import ImageView
import numpy as np
import cv2
import cv2.aruco as aruco
from views import Ui_MainWindow, Ui_New_FPTV_value_Window

import Camera
import Guide
import Warehouse


class Main_function(QMainWindow, Ui_MainWindow):
    sig2 = pyqtSignal(object)

    def __init__(self):
        super(self.__class__, self).__init__()
        print("Tworzę Main Function")
        self.setupUi(self)
        self.id_robot = None
        self.robot_id_selected = False
        self.id_aim = None
        self.id_aim_selected = False
        self.id_pallet = None
        self.id_warehouse = 26
        self.pallet_id_selected = False
        self.markers_number = None
        self.FPTV = 25
        self.PORT = "COM14"
        self.BAUDRATE = 9600
        self.guideinitialized = False
        self.guide = None
        self.camera = Camera.Camera(1)
        self.camera.Initialize()
        self.tableWidget.item(0,1).setBackground(QColor(169,245,169))
        self.tableWidget.item(0, 1).setText("OK")
        self.tableWidget2.item(0, 1).setText("1")
        self.tableWidget2.item(1, 1).setText(self.PORT)
        self.tableWidget2.item(2, 1).setText(str(self.BAUDRATE))
        self.tableWidget2.item(3, 1).setText(str(self.FPTV))

        self.Start_frame()
        self.ViewisRunning = False
        self.View3isRunning = False
        self.PalletizationisRunning = False
        self.pushButton_GO.setEnabled(False)
        self.pushButton_View1.clicked.connect(self.start_View1)
        self.pushButton_View2.clicked.connect(self.start_View2)
        self.pushButton_View3.clicked.connect(self.start_View3)
        self.pushButton_GO.clicked.connect(self.Start_Palletization)
        self.Select_robot_id_button.clicked.connect(self.Select_Robot_Id)
        self.Select_pallet_id_button.clicked.connect(self.Select_Pallet_Id)
        self.Robot_id_box.setText("0")
        self.Pallet_id_box.setText("2")
        self.actionChange_FPTV.triggered.connect(self.ACTION_Change_FPTV)

    def Start_frame(self):
        if self.camera.initialized:
            self.camera.get_frame()
            corners, ids = self.camera.Detect_Markers(self.camera.frame)
            if np.all(ids != None):
                self.markers_number = len(ids)
                self.camera.frame= self.camera.Print_Detected_Markers(self.camera.frame, corners, ids)
                cv2.putText(self.camera.frame, "Real view", (70,70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255),2)


                # cv2.circle(self.camera.frame, (366,0), 2, (252, 223, 3), 2)
                # cv2.circle(self.camera.frame, (450, 0), 2, (252, 223, 3), 2)
                # cv2.circle(self.camera.frame, (450,88), 2, (252, 223, 3), 2)
                # cv2.circle(self.camera.frame, (366,88), 2, (252, 223, 3), 2)



                self.update_View(self.camera.frame)
            else:
                cv2.putText(self.camera.frame, "!No Markers Detected!", (70,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
                self.update_View(self.camera.frame)

            # self.camera.close_camera()

    def update_View(self, frame):
        self.image_view.view.invertX(True)
        self.image_view.setImage(np.rot90(frame))

    def start_View1(self):
        if self.ViewisRunning == False:
            # if self.camera.initialized == False: self.camera.Initialize()
            if self.camera.initialized == True:
                if self.PalletizationisRunning:  self.PalletizaionThread.VIEW_IS_RUNNING = True
                self.View1Thread = Camera.VideoStreem_View1_Thread(self.camera)
                self.ViewisRunning = True
                self.pushButton_View1.setText("View 1 - Running")
                self.pushButton_View1.setStyleSheet("background-color: #A9F5A9")
                self.pushButton_View2.setEnabled(False)
                self.pushButton_View3.setEnabled(False)
                # self.pushButton_View4.setEnabled(False)
                # self.pushButton_View5.setEnabled(False)
                self.View1Thread.start()
                self.View1Thread.sig_View1_Thread_frame.connect(self.update_View)
        else:
            self.View1Thread.runperm = False
            self.ViewisRunning = False
            if self.PalletizationisRunning:  self.PalletizaionThread.VIEW_IS_RUNNING = False
            #self.camera.close_camera()
            #self.camera.initialized = False
            self.pushButton_View1.setText("View 1")
            self.pushButton_View1.setStyleSheet("background-color: DEFAULT <later on>")
            self.pushButton_View2.setEnabled(True)
            self.pushButton_View3.setEnabled(True)
            # self.pushButton_View4.setEnabled(True)
            # self.pushButton_View5.setEnabled(True)

    def start_View2(self):
        if self.ViewisRunning == False:
            # if self.camera.initialized == False: self.camera.Initialize()
            if self.camera.initialized == True:
                if self.PalletizationisRunning:  self.PalletizaionThread.VIEW_IS_RUNNING = True

                self.View2Thread = Camera.VideoStreem_View2_Thread(self.camera)
                self.ViewisRunning = True
                self.pushButton_View2.setText("View 2 - Running")
                self.pushButton_View2.setStyleSheet("background-color: #A9F5A9")
                self.pushButton_View1.setEnabled(False)
                self.pushButton_View3.setEnabled(False)
                # self.pushButton_View4.setEnabled(False)
                # self.pushButton_View5.setEnabled(False)
                self.View2Thread.start()
                self.View2Thread.sig_View2_Thread_frame.connect(self.update_View)
        else:
            self.View2Thread.runperm = False
            self.ViewisRunning = False
            if self.PalletizationisRunning:  self.PalletizaionThread.VIEW_IS_RUNNING = False

            #self.camera.close_camera()
            #self.camera.initialized = False
            self.pushButton_View2.setText("View 2")
            self.pushButton_View2.setStyleSheet("background-color: DEFAULT <later on>")
            self.pushButton_View1.setEnabled(True)
            self.pushButton_View3.setEnabled(True)
            # self.pushButton_View4.setEnabled(True)
            # self.pushButton_View5.setEnabled(True)

    def Select_Robot_Id(self):
        if self.robot_id_selected == False:
            tmp = self.Robot_id_box.text()
            if tmp.isdigit() != True:
                QMessageBox.about(self, "Error", "Robot id is not a number!")
                self.Robot_id_box.clear()
                return 0
            if tmp == self.id_pallet:
                QMessageBox.about(self, "Error", "You already choose this id for pallet!")
                self.Robot_id_box.clear()
                return 0
            self.id_robot = int(tmp)
            self.robot_id_selected = True
            self.Robot_id_box.setAlignment(Qt.AlignCenter)
            self.Robot_id_box.setStyleSheet("background-color: #A9F5A9")
            self.Robot_id_box.setEnabled(False)
            self.Select_robot_id_button.setText("Reset")
            if self.pallet_id_selected == True:
                self.pushButton_GO.setEnabled(True)
        elif self.robot_id_selected == True:
            self.id_robot = None
            self.robot_id_selected = False
            self.Robot_id_box.setEnabled(True)
            self.Robot_id_box.setAlignment(Qt.AlignLeft)
            self.Robot_id_box.clear()
            self.Robot_id_box.setStyleSheet("background-color: : DEFAULT <later on>")
            self.Select_robot_id_button.setText("Select")
            self.pushButton_GO.setEnabled(False)

    def Select_Pallet_Id(self):
        if self.pallet_id_selected == False:
            tmp = self.Pallet_id_box.text()
            if tmp.isdigit() != True:
                QMessageBox.about(self, "Error", "Pallet id is not a number!")
                self.Pallet_id_box.clear()
                return 0
            if tmp == self.id_robot:
                QMessageBox.about(self, "Error", "You already choose this id for robot!")
                self.Pallet_id_box.clear()
                return 0
            self.id_pallet = int(tmp)

            self.pallet_id_selected = True
            self.Pallet_id_box.setAlignment(Qt.AlignCenter)
            self.Pallet_id_box.setStyleSheet("background-color: #A9F5A9")
            self.Pallet_id_box.setEnabled(False)
            self.Select_pallet_id_button.setText("Reset")
            if self.robot_id_selected == True:
                self.pushButton_GO.setEnabled(True)

        elif self.pallet_id_selected == True:
            self.pallet_id_selected = False
            self.id_pallet = None
            self.Pallet_id_box.setEnabled(True)
            self.Pallet_id_box.setAlignment(Qt.AlignLeft)
            self.Pallet_id_box.clear()
            self.Pallet_id_box.setStyleSheet("background-color: : DEFAULT <later on>")
            self.Select_pallet_id_button.setText("Select")
            self.pushButton_GO.setEnabled(False)

    def Start_Palletization(self):
        if self.PalletizationisRunning == False:
            self.pushButton_GO.setText("STOP")
            self.pushButton_GO.setStyleSheet("background-color: #A9F5A9")
            self.id_aim = self.id_pallet
            if self.guideinitialized == False:
                self.guide = Guide.Guide(self.camera, self.FPTV, self.PORT, self.BAUDRATE)
                if self.guide.guide_ready == True:
                    self.guideinitialized = True
                else:
                    print("Nie mogę rozpocząć paletyzacji. Error: Guide nie jest zainicjalizowany")
                    self.tableWidget.item(1, 1).setBackground(QColor(255, 51, 51))
                    self.tableWidget.item(1, 1).setText("Error")
                    self.tableWidget.item(2, 1).setBackground(QColor(255, 51, 51))
                    self.tableWidget.item(2, 1).setText("Error")

                    self.pushButton_GO.setText("START")
                    self.pushButton_GO.setStyleSheet("background-color: DEFAULT <later on>")
                    return 0
            print("Wywołuję wątek")

            self.PalletizaionThread = Guide.Guide_Thread(self.camera, self.guide, self.id_robot, self.id_aim, 30, 3, self.ViewisRunning)
            self.PalletizaionThread.setPriority(QThread.HighestPriority)
            self.PalletizationisRunning = True
            self.PalletizaionThread.start()
            self.PalletizaionThread.sig_Guide_Thread_Frame_With_Road.connect(self.update_View3)
            self.PalletizaionThread.sig_Guide_Thread_ProgressBar_MaxValue.connect(self.Set_Maximum_ProgressBar)
            self.PalletizaionThread.sig_Guide_Thread_ProgressBar_NewValue.connect(self.Update_ProgressBar)
            self.PalletizaionThread.sig_Guide_Thread_Initialized.connect(self.UpdateTable)
        else:
            self.PalletizationisRunning = False
            self.PalletizaionThread.runperm = False
            self.PalletizaionThread.terminate()
            self.guide.communication.Serial.close()
            del self.guide
            self.guideinitialized = False
            self.tableWidget.item(1, 1).setText("No initialized")
            self.tableWidget.item(2, 1).setText("No initialized")
            self.tableWidget.item(1, 1).setBackground(QColor(255, 255, 255))
            self.tableWidget.item(2, 1).setBackground(QColor(255, 255, 255))

            self.ProgressBar.setValue(0)
            self.pushButton_GO.setText("START")
            self.pushButton_GO.setStyleSheet("background-color: DEFAULT <later on>")

    def Set_Maximum_ProgressBar(self, value):
        self.ProgressBar.setMaximum(value)

    def Update_ProgressBar(self, value):
        self.ProgressBar.setValue(value)

    def start_View3(self):
        if self.View3isRunning == False:
            self.View3isRunning = True
            self.pushButton_View3.setText("View 3 - Running")
            self.pushButton_View3.setStyleSheet("background-color: #A9F5A9")
            self.pushButton_View1.setEnabled(False)
            self.pushButton_View2.setEnabled(False)
        else:
            self.View3isRunning = False
            self.pushButton_View3.setText("View 3")
            self.pushButton_View3.setStyleSheet("background-color: DEFAULT <later on>")
            self.pushButton_View1.setEnabled(True)
            self.pushButton_View2.setEnabled(True)

    def update_View3(self, frame):
        if self.View3isRunning == True:
            self.image_view.view.invertX(True)
            self.image_view.setImage(np.rot90(frame))

    def UpdateTable(self, ok):
        self.tableWidget.item(1, 1).setBackground(QColor(169,245,169))
        self.tableWidget.item(1, 1).setText("OK")
        self.tableWidget.item(2, 1).setBackground(QColor(169,245,169))
        self.tableWidget.item(2, 1).setText("OK")

        print(ok)

    def ACTION_Change_FPTV(self):
        self.FPTV_dialog = Ui_New_FPTV_value_Window(self)
        self.FPTV_dialog.show()
        self.FPTV_dialog.sig_Change_FPTV.connect(self.UpdateFPTV)

    def UpdateFPTV(self, value):
        self.FPTV = value
        self.tableWidget2.item(3, 1).setText(str(self.FPTV))



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    MainWindow = Main_function()
    MainWindow.show()
    app.exit(app.exec_())