from PyQt5.QtCore import Qt, QThread, QTimer, QRect, QMetaObject, QCoreApplication, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QSizePolicy, QMessageBox
from PyQt5.QtGui import QImage, QColor
from pyqtgraph import ImageView
import numpy as np
import cv2
import cv2.aruco as aruco
from views import Ui_MainWindow

import Camera


class Main_function(QMainWindow, Ui_MainWindow):
    sig2 = pyqtSignal(object)

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.id_robot = None
        self.robot_id_selected = False
        self.id_aim = None
        self.id_aim_selected = False
        self.id_pallet = None
        self.pallet_id_selected = False
        self.markers_number = None
        self.camera = Camera.Camera(1)
        self.Start_frame()
        self.ViewisRunning = False

        self.pushButton_GO.setEnabled(False)
        self.pushButton_View1.clicked.connect(self.start_View1)
        self.pushButton_View2.clicked.connect(self.start_View2)
        # self.pushButton_Wyznacz_Trajektorie.connect(self.Start_palletizaion)
        self.Select_robot_id_button.clicked.connect(self.Select_Robot_Id)
        self.Select_pallet_id_button.clicked.connect(self.Select_Pallet_Id)


    def Start_frame(self):
        self.camera.Initialize()
        if self.camera.initialized:
            self.camera.get_frame()
            corners, ids = self.camera.Detect_Markers(self.camera.frame)
            if np.all(ids != None):
                self.markers_number = len(ids)
                self.camera.frame= self.camera.Print_Detected_Markers(self.camera.frame, corners, ids)
                cv2.putText(self.camera.frame, "Real view", (70,70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255),2)
                self.update_View(self.camera.frame)
            else:
                cv2.putText(self.camera.frame, "!No Markers Detected!", (70,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
                self.update_View(self.camera.frame)

            self.camera.close_camera()

    def update_View(self, frame):
        self.image_view.setImage(frame.T)

    def start_View1(self):
        if self.ViewisRunning == False:
            if self.camera.initialized == False: self.camera.Initialize()
            if self.camera.initialized == True:
                self.View1Thread = Camera.VideoStreem_View1_Thread(self.camera)
                self.ViewisRunning = True
                self.pushButton_View1.setText("View1 - Running")
                self.pushButton_View1.setStyleSheet("background-color: #A9F5A9")
                self.pushButton_View2.setEnabled(False)
                self.pushButton_View3.setEnabled(False)
                self.pushButton_View4.setEnabled(False)
                self.pushButton_View5.setEnabled(False)
                self.View1Thread.start()
                self.View1Thread.sig_View1_Thread_frame.connect(self.update_View)
        else:
            self.View1Thread.runperm = False
            self.ViewisRunning = False
            self.camera.close_camera()
            self.camera.initialized = False
            self.pushButton_View1.setText("View1")
            self.pushButton_View1.setStyleSheet("background-color: DEFAULT <later on>")
            self.pushButton_View2.setEnabled(True)
            self.pushButton_View3.setEnabled(True)
            self.pushButton_View4.setEnabled(True)
            self.pushButton_View5.setEnabled(True)

    def start_View2(self):
        if self.ViewisRunning == False:
            if self.camera.initialized == False: self.camera.Initialize()
            if self.camera.initialized == True:
                self.View2Thread = Camera.VideoStreem_View2_Thread(self.camera)
                self.ViewisRunning = True
                self.pushButton_View2.setText("View2 - Running")
                self.pushButton_View2.setStyleSheet("background-color: #A9F5A9")
                self.pushButton_View1.setEnabled(False)
                self.pushButton_View3.setEnabled(False)
                self.pushButton_View4.setEnabled(False)
                self.pushButton_View5.setEnabled(False)
                self.View2Thread.start()
                self.View2Thread.sig_View2_Thread_frame.connect(self.update_View)
        else:
            self.View2Thread.runperm = False
            self.ViewisRunning = False
            self.camera.close_camera()
            self.camera.initialized = False
            self.pushButton_View2.setText("View2")
            self.pushButton_View2.setStyleSheet("background-color: DEFAULT <later on>")
            self.pushButton_View1.setEnabled(True)
            self.pushButton_View3.setEnabled(True)
            self.pushButton_View4.setEnabled(True)
            self.pushButton_View5.setEnabled(True)

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


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    MainWindow = Main_function()
    MainWindow.show()
    app.exit(app.exec_())