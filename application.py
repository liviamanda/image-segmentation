from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QTextImageFormat, QImageReader
from PyQt6.QtCore import QUrl, QVariant
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QFileDialog
from PIL import Image, ImageQt
from pathlib import Path
import sys
import glob
import cv2
import sys, os, csv
os.environ["SM_FRAMEWORK"] = "tf.keras"
import tensorflow as tf
import segmentation_models as sm
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
import keras 
from keras.utils import normalize
from keras.metrics import MeanIoU
from keras.models import load_model
from skimage.transform import (hough_line, hough_line_peaks,
                               probabilistic_hough_line)
from skimage.feature import canny
from skimage import data
from pylab import imread, imshow, gray, mean
from datetime import datetime



class Ui_MainWindow(object):
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.frame_3 = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(parent=self.frame_3)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.gridLayout_3.addWidget(self.frame_3, 0, 0, 1, 2)
        self.frame_2 = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 2, 2, 1, 1)
        self.source = QtWidgets.QLabel(parent=self.frame_2)
        self.source.setMinimumSize(QtCore.QSize(280, 280))
        self.source.setMaximumSize(QtCore.QSize(280, 280))
        self.source.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.source.setText("")
        self.source.setObjectName("source")
        self.gridLayout_2.addWidget(self.source, 1, 0, 1, 1)
        self.nsaResult = QtWidgets.QLabel(parent=self.frame_2)
        self.nsaResult.setMinimumSize(QtCore.QSize(280, 280))
        self.nsaResult.setMaximumSize(QtCore.QSize(280, 280))
        self.nsaResult.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.nsaResult.setText("")
        self.nsaResult.setObjectName("nsaResult")
        self.gridLayout_2.addWidget(self.nsaResult, 3, 2, 1, 1)
        self.segmentation = QtWidgets.QLabel(parent=self.frame_2)
        self.segmentation.setMinimumSize(QtCore.QSize(280, 280))
        self.segmentation.setMaximumSize(QtCore.QSize(280, 280))
        self.segmentation.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.segmentation.setText("")
        self.segmentation.setObjectName("segmentation")
        self.gridLayout_2.addWidget(self.segmentation, 3, 0, 1, 1)
        self.preProcessing = QtWidgets.QLabel(parent=self.frame_2)
        self.preProcessing.setMinimumSize(QtCore.QSize(280, 280))
        self.preProcessing.setMaximumSize(QtCore.QSize(280, 280))
        self.preProcessing.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.preProcessing.setText("")
        self.preProcessing.setObjectName("preProcessing")
        self.gridLayout_2.addWidget(self.preProcessing, 1, 2, 1, 1)
        self.gridLayout_3.addWidget(self.frame_2, 1, 0, 1, 1)
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_7 = QtWidgets.QLabel(parent=self.frame)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_3.addWidget(self.label_7)
        self.frame_4 = QtWidgets.QFrame(parent=self.frame)
        self.frame_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.folderPath = QtWidgets.QLineEdit(parent=self.frame_4)
        self.folderPath.setObjectName("folderPath")
        self.horizontalLayout_3.addWidget(self.folderPath)
        self.btnBrowseFolder = QtWidgets.QPushButton(parent=self.frame_4)
        self.btnBrowseFolder.setObjectName("btnBrowseFolder")
        self.horizontalLayout_3.addWidget(self.btnBrowseFolder)
        self.btnOpenFolder = QtWidgets.QPushButton(parent=self.frame_4)
        self.btnOpenFolder.setObjectName("btnOpenFolder")
        self.horizontalLayout_3.addWidget(self.btnOpenFolder)
        self.verticalLayout_3.addWidget(self.frame_4)
        self.label_6 = QtWidgets.QLabel(parent=self.frame)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_3.addWidget(self.label_6)
        self.frame_7 = QtWidgets.QFrame(parent=self.frame)
        self.frame_7.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.btnResnet = QtWidgets.QPushButton(parent=self.frame_7)
        self.btnResnet.setObjectName("btnResnet")
        self.horizontalLayout_5.addWidget(self.btnResnet)
        self.btnInception = QtWidgets.QPushButton(parent=self.frame_7)
        self.btnInception.setObjectName("btnInception")
        self.horizontalLayout_5.addWidget(self.btnInception)
        self.btnEfficientnet = QtWidgets.QPushButton(parent=self.frame_7)
        self.btnEfficientnet.setObjectName("btnEfficientnet")
        self.horizontalLayout_5.addWidget(self.btnEfficientnet)
        self.modelPath = QtWidgets.QLineEdit(parent=self.frame_7)
        self.modelPath.setReadOnly(True)
        self.modelPath.setObjectName("modelPath")
        self.horizontalLayout_5.addWidget(self.modelPath)
        self.verticalLayout_3.addWidget(self.frame_7)
        self.label_8 = QtWidgets.QLabel(parent=self.frame)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_3.addWidget(self.label_8)
        self.frame_5 = QtWidgets.QFrame(parent=self.frame)
        self.frame_5.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_4.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.listImage = QtWidgets.QListWidget(parent=self.frame_5)
        self.listImage.setObjectName("listImage")
        self.horizontalLayout_4.addWidget(self.listImage)
        self.frame_6 = QtWidgets.QFrame(parent=self.frame_5)
        self.frame_6.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout_4.setContentsMargins(10, 0, 10, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.btnCalculate = QtWidgets.QPushButton(parent=self.frame_6)
        self.btnCalculate.setObjectName("btnCalculate")
        self.verticalLayout_4.addWidget(self.btnCalculate)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.btnClear = QtWidgets.QPushButton(parent=self.frame_6)
        self.btnClear.setObjectName("btnClear")
        self.verticalLayout_4.addWidget(self.btnClear)
        self.horizontalLayout_4.addWidget(self.frame_6)
        self.verticalLayout_3.addWidget(self.frame_5)
        self.label_9 = QtWidgets.QLabel(parent=self.frame)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_3.addWidget(self.label_9)
        self.tableResult = QtWidgets.QTableWidget(parent=self.frame)
        self.tableResult.setObjectName("tableResult")
        self.tableResult.setColumnCount(5)
        self.tableResult.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableResult.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableResult.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableResult.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableResult.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableResult.setHorizontalHeaderItem(4, item)
        self.tableResult.horizontalHeader().setCascadingSectionResizes(True)
        self.tableResult.verticalHeader().setDefaultSectionSize(20)
        self.tableResult.verticalHeader().setMinimumSectionSize(20)
        self.tableResult.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_3.addWidget(self.tableResult)
        self.frame_8 = QtWidgets.QFrame(parent=self.frame)
        self.frame_8.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_8)
        self.horizontalLayout_6.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem1 = QtWidgets.QSpacerItem(485, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.btnSave = QtWidgets.QPushButton(parent=self.frame_8)
        self.btnSave.setObjectName("btnSave")
        self.horizontalLayout_6.addWidget(self.btnSave)
        self.verticalLayout_3.addWidget(self.frame_8)
        self.gridLayout_3.addWidget(self.frame, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.folderPath.setEnabled(False)
        self.modelPath.setEnabled(False)
        
        self.btnBrowseFolder.clicked.connect(self.open_file_dialog)
        self.btnOpenFolder.clicked.connect(self.select_file_dialog)
        self.btnClear.clicked.connect(self.clear_file_dialog)
        self.btnResnet.clicked.connect(self.get_model_resnet34)
        self.btnInception.clicked.connect(self.get_model_inceptionv3)
        self.btnEfficientnet.clicked.connect(self.get_model_efficientnetb7)
        self.btnCalculate.clicked.connect(self.get_image_path)
        self.btnSave.clicked.connect(self.handleSave)
        
    def handleSave(self):
        path, ok = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save CSV', os.getenv('HOME'), 'CSV(*.csv)')
        if ok:
            columns = range(self.tableResult.columnCount())
            header = [self.tableResult.horizontalHeaderItem(column).text()
                      for column in columns]
            with open(path, 'w') as csvfile:
                writer = csv.writer(
                    csvfile, dialect='excel', lineterminator='\n')
                writer.writerow(header)
                for row in range(self.tableResult.rowCount()):
                    writer.writerow(
                        self.tableResult.item(row, column).text()
                        for column in columns)
        
        
    def open_file_dialog(self):
        dir_name = QFileDialog.getExistingDirectory()
        
        if dir_name:
            path = Path(dir_name)
            self.folderPath.setText(dir_name)
    
    def select_file_dialog(self):
        path = self.folderPath.text()
        dir = QtCore.QDir(path)
        for file in dir.entryList():
            self.listImage.addItem(file)    
            
    def clear_file_dialog(self):
        self.listImage.clear()
        
    def get_model_resnet34(self):
        self.modelPath.setText('C:/Users/septi/OneDrive/Projects/Livia/app/model/resnet34.hdf5')
        
    def get_model_inceptionv3(self):
        self.modelPath.setText('C:/Users/septi/OneDrive/Projects/Livia/app/model/inceptionv3.hdf5')
    
    def get_model_efficientnetb7(self):
        self.modelPath.setText('C:/Users/septi/OneDrive/Projects/Livia/app/model/efficientnetb7.hdf5')
    global datas
    datas = []
    def get_image_path(self):
        image_path = self.folderPath.text() + '/' + str(self.listImage.currentItem().text())
        pixmap = QtGui.QPixmap(image_path)  # Replace 'your_image.png' with your image file path
        pixmap = pixmap.scaled(280, 280)
        
        self.source.setPixmap(pixmap)
        
        # Split the path by '/' to separate the components
        path_components = self.modelPath.text().split('/')

        # Get the last component (the filename) and remove the file extension
        filename = path_components[-1].split('.')[0]
        
        if(filename=="resnet34"):
            BACKBONE = 'resnet34'
        elif(filename=="inceptionv3"):
            BACKBONE = 'inceptionv3'
        elif(filename=="efficientnetb7"):
            BACKBONE ='efficientnetb7'
        else :
            BACKBONE = 'not defined'
            
        preprocess_input = sm.get_preprocessing(BACKBONE)
        
        img = tf.io.read_file(image_path)
        img = tf.image.decode_jpeg(img, channels=3)
        img = tf.image.resize(img, (512, 512))
    
        preproImage = preprocess_input(img)
        
        if(filename=="resnet34"):
            imgpil = tf.keras.preprocessing.image.img_to_array(preproImage)
            plt.figure(figsize=(20,10))
            plt.axis('off')
            plt.imshow(preproImage[:,:,1])
            plt.savefig('prep_img.jpg', bbox_inches='tight')
        else:
            imgpil = tf.keras.preprocessing.image.img_to_array(preproImage)
            plt.figure(figsize=(20,10))
            plt.axis('off')
            plt.imshow(imgpil)
            plt.savefig('prep_img.jpg', bbox_inches='tight')
        
        img = np.expand_dims(preproImage, 0)
        dimImg = []
        
        model = load_model(self.modelPath.text(), compile=False) 
        dimImg.append(img)
        
        predImg = model.predict(dimImg, verbose=0)
        plt.figure(figsize=(20,10))
        plt.axis('off')
        plt.imshow(predImg[0,:,:,1],cmap='gray')
        plt.imsave('./seg_img.jpg', predImg[0,:,:,1], cmap='gray')
        
        pixmap2 = QtGui.QPixmap('./prep_img.jpg')  # Replace 'your_image.png' with your image file path
        pixmap2 = pixmap2.scaled(280, 280)
        self.preProcessing.setPixmap(pixmap2)
        
        pixmap3 = QtGui.QPixmap('./seg_img.jpg',)  # Replace 'your_image.png' with your image file path
        pixmap3 = pixmap3.scaled(280, 280)
        self.segmentation.setPixmap(pixmap3)
        
        #FSA Calculation
        image_path = self.folderPath.text() + '/' + str(self.listImage.currentItem().text())
        img = cv2.imread('./seg_img.jpg', cv2.IMREAD_GRAYSCALE)
        result_temp = img.copy()
        result_temp = cv2.resize(img,(1404,1404),interpolation = cv2.INTER_AREA)*0+255
        original_img = cv2.imread('./seg_img.jpg', cv2.IMREAD_GRAYSCALE)
        ori = cv2.imread('./seg_img.jpg', cv2.IMREAD_GRAYSCALE)
        dim = (1404, 1404)
        img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        original_img= cv2.resize(original_img, dim, interpolation = cv2.INTER_AREA)
        ori= cv2.resize(ori, dim, interpolation = cv2.INTER_AREA)
        img_blur = cv2.GaussianBlur(img, (5,5), 0)
        circles = cv2.HoughCircles(img_blur, cv2.HOUGH_GRADIENT, 2, 100, param1=40, param2=56, minRadius=80, maxRadius=0)
        mask = np.zeros(img.shape[:2], dtype=np.uint8)+255
        center_value = []
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            j , k = np.shape(circles)
            if j>1 :
                circles = [circles[0][:]]
            for (x, y, r) in circles:
                cv2.circle(ori, (x, y), r, (0, 255, 0), 2)
                center_value = (x,y)
                cv2.circle(ori, (x, y), 2, (0, 0, 255), 3)
                cv2.circle(mask, (x, y), r+40, (0, 0, 0),-1)
                cor_circle = (x,y)
        result = cv2.bitwise_and(img, mask)
        plt.axis('off')
        imgplot = plt.imshow(result)
        plt.imsave('./body.jpg', result, cmap='gray')
        temp = (img.copy()*0)
        res_temp = cv2.bitwise_and(temp, mask)
        edges = cv2.Canny(mask, 50, 150)
        rows, cols = np.where(edges > 250)
        values_above_250 = edges[rows, cols]
        data_above_250 = np.column_stack((rows, cols, values_above_250))
        data_above_250_second_image = []
        for item in data_above_250:
            row, col, pixel_value = item   
            if img[row, col] > 250:
                data_above_250_second_image.append((row,col)) 
        for item in data_above_250_second_image:
            row, col = item
            img[row,col] = 0
        cv2.line(img, (data_above_250_second_image[0][1],data_above_250_second_image[0][0]),  (data_above_250_second_image[-1][1],data_above_250_second_image[-1][0]), (0,0,0), 5) 
        
        
        
        
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        edge_points = []
        # Calculate the middle point of the line
        middle_point = ((data_above_250_second_image[0][1]+data_above_250_second_image[-1][1])//2, (data_above_250_second_image[0][0]+data_above_250_second_image[-1][0])//2)

        # Define the two endpoints of the line
        pt1 = (middle_point[0], middle_point[1])
        pt2 = (cor_circle[0],cor_circle[1])

        # Calculate the slope of the line
        m = (pt2[1] - pt1[1]) / (pt2[0] - pt1[0])


        # Calculate the y-intercept of the line
        b = pt1[1] - m * pt1[0]


        # Determine the x-coordinates where the line intersects with the edges of the frame
        x1 = 0
        y1 = m * x1 + b

        x2 = 3000
        y2 = m * x2 + b

        # Draw the new line
        cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 0), 5)
        cv2.line(result_temp, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 0), 4)
        
        image_path = "C:/Users/septi/OneDrive/Projects/Livia/app/body.jpg"
        img2 = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        height, width = img2.shape[:2]
        top_60_percent = int(0.6 * height)
        img2[:top_60_percent, :] = 0
        img2 = cv2.GaussianBlur(img2,(5,5),cv2.BORDER_DEFAULT)
        edges = cv2.Canny(img2, 20, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        result_img = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
        for contour in contours:
            for point in contour:
                # Extract x, y coordinates
                x, y = point[0]

                # Create points with a distance of 5 pixels
                for dx in range(-5, 6):
                    for dy in range(-5, 6):
                        new_x, new_y = x + dx, y + dy

                        # Check if the new point is within the image bounds
                        if 0 <= new_x < img2.shape[1] and 0 <= new_y < img2.shape[0]:
                            # Draw the points on the result image
                            result_img[new_y, new_x] = [0, 0, 0]  # Red color for visualization

        img_bin = (img2>128).astype(np.uint8)
        contours, _ = cv2.findContours(img_bin, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)

        # Determine center of gravity and orientation using Moments
        M = cv2.moments(contours[0])
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        theta = 0.5*np.arctan2(2*M["mu11"],M["mu20"]-M["mu02"])

        endx = center[1] * np.cos(theta) + center[0] 
        endy = center[1] * np.sin(theta) + center[1] 
        endxx = (center[1]-1404) * np.cos(theta) + center[0] 
        endyy = (center[1]-1404) * np.sin(theta) + center[1] 

        if theta>0:
            endx = (1404-center[1]) * np.cos(theta) + center[0] 
            endy = (1404-center[1]) * np.sin(theta) + center[1] 
            endxx = (-(center[1])) * np.cos(theta) + center[0] 
            endyy = (-(center[1])) * np.sin(theta) + center[1] 
        
        plt.figure(figsize=(10,10))
        plt.axis('off')
        imgplot = plt.imshow(img,cmap='gray')
        plt.plot([center[0],  endx,endxx], [center[1],  endy,endyy],color="black",linewidth=4)
        plt.margins(x=0,y=0)
        plt.savefig('./fsa_result.jpg',bbox_inches='tight')
        
        pixmap4 = QtGui.QPixmap('./fsa_result.jpg')  # Replace 'your_image.png' with your image file path
        pixmap4 = pixmap4.scaled(280, 280)
        self.nsaResult.setPixmap(pixmap4)
        
        
        plt.axis('off')
        imgplot = plt.imshow(result_temp,cmap='gray')
        plt.plot([center[0],  endx,endxx], [center[1],  endy,endyy],color="black",linewidth=1)
        plt.margins(x=0,y=0)
        plt.savefig('./angle.jpg',bbox_inches='tight')
        
        image = imread('./angle.jpg')
        image = np.mean(image,axis=2)
        image = (image < 128)*255
        h, theta, d = hough_line(image)
        
        fig, axes = plt.subplots(1, 3, figsize=(15, 6),
                         subplot_kw={'adjustable': 'box'})
        ax = axes.ravel()

        ax[0].imshow(image, cmap=cm.gray)
        ax[0].set_title('Input image')
        ax[0].set_axis_off()
        ax[1].imshow(np.log(1 + h),
                    extent=[np.rad2deg(theta[-1]), np.rad2deg(theta[0]), d[-1], d[0]],
                    cmap=cm.gray, aspect=1/1.5)
        ax[1].set_title('Hough transform')
        ax[1].set_xlabel('Angles (degrees)')
        ax[1].set_ylabel('Distance (pixels)')
        ax[1].axis('image')

        ax[2].imshow(image, cmap=cm.gray)

        for _, angle, dist in zip(*hough_line_peaks(h, theta, d)):
            y0 = (dist - 0 * np.cos(angle)) / np.sin(angle)
            y1 = (dist - image.shape[1] * np.cos(angle)) / np.sin(angle)
            ax[2].plot((0, image.shape[1]), (y0, y1), '-r')
        ax[2].set_xlim((0, image.shape[1]))
        ax[2].set_ylim((image.shape[0], 0))
        ax[2].set_axis_off()
        ax[2].set_title('Detected lines')

        plt.tight_layout()
        

        angle=[]
        dist=[]
        for _, a , d in zip(*hough_line_peaks(h, theta, d)):
            angle.append(a)
            dist.append(d)

        angle = [a*180/np.pi for a in angle]
        angle_reel = 180 - (np.max(angle) - np.min(angle))
        now = datetime.now()
        datas.append({"No":"","Date":f'{now.strftime("%Y-%m-%d %H:%M:%S")}',"Name":f'{self.listImage.currentItem().text()}',"Backbone":f'{filename}',"Result":f'{angle_reel}'})
        row = 0
        self.tableResult.setRowCount(len(datas))
        for data in datas:
            self.tableResult.setItem(row,0,QtWidgets.QTableWidgetItem(str(row+1)))
            self.tableResult.setItem(row,1,QtWidgets.QTableWidgetItem(data["Date"]))
            self.tableResult.setItem(row,2,QtWidgets.QTableWidgetItem(data["Name"]))
            self.tableResult.setItem(row,3,QtWidgets.QTableWidgetItem(data["Backbone"]))
            self.tableResult.setItem(row,4,QtWidgets.QTableWidgetItem(data["Result"]))
            row = row +1 
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "APLIKASI PERHITUNGAN FEMORAL NECK-SHAFT ANGLE OTOMATIS PADA CITRA RADIOGRAFI PELVIS DENGAN HOUGH TRANSFORM DAN EFF-UNET"))
        self.label_2.setText(_translate("MainWindow", "Source"))
        self.label_3.setText(_translate("MainWindow", "Pre-processing"))
        self.label_4.setText(_translate("MainWindow", "Segmentation"))
        self.label_5.setText(_translate("MainWindow", "NSA Result"))
        self.label_7.setText(_translate("MainWindow", "Input Image Folder "))
        self.btnBrowseFolder.setText(_translate("MainWindow", "Browse"))
        self.btnOpenFolder.setText(_translate("MainWindow", "Select"))
        self.label_6.setText(_translate("MainWindow", "Select Segmentation Method"))
        self.btnResnet.setText(_translate("MainWindow", "Resnet34"))
        self.btnInception.setText(_translate("MainWindow", "Inceptionv3"))
        self.btnEfficientnet.setText(_translate("MainWindow", "Efficientnetb7"))
        self.label_8.setText(_translate("MainWindow", "Select Image"))
        self.btnCalculate.setText(_translate("MainWindow", "Calculate"))
        self.btnClear.setText(_translate("MainWindow", "Clear all"))
        self.label_9.setText(_translate("MainWindow", "History"))
        item = self.tableResult.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "No"))
        item = self.tableResult.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Date"))
        item = self.tableResult.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Name"))
        item = self.tableResult.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Backbone"))
        item = self.tableResult.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Result"))
        self.btnSave.setText(_translate("MainWindow", "Save"))

if __name__=="__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
