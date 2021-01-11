from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, cam):
        QThread.__init__(self, cam)
        self.cam = cam

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(self.cam)
        while True:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt live label demo")
        self.disply_width = 640
        self.display_height = 480
        # create the label that holds the image
        self.cam1_label = QLabel(self)
        self.cam1_label.resize(self.disply_width, self.display_height)
        # create a text label
        self.textLabelCam1 = QLabel('Webcam')

        self.cam2_label = QLabel(self)
        self.cam2_label.resize(self.disply_width, self.display_height)
        # create a text label
        self.textLabelCam2 = QLabel('Webcam')

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.cam1_label)
        vbox.addWidget(self.textLabelCam1)
        vbox.addWidget(self.cam2_label)
        vbox.addWidget(self.textLabelCam2)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        # create the video capture thread
        self.thread1 = VideoThread('20180910_144521.mp4')
        # connect its signal to the update_image slot
        self.thread1.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread1.start()

        # create the video capture thread CAM2
        self.thread2 = VideoThread('20180910_144521.mp4')
        # connect its signal to the update_image slot
        self.thread2.change_pixmap_signal.connect(self.update_image2)
        # start the thread
        self.thread2.start()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.cam1_label.setPixmap(qt_img)

    @pyqtSlot(np.ndarray)
    def update_image2(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.cam2_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

#
if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())
