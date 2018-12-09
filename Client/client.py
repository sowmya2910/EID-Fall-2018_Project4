# -*- coding: utf-8 -*-
# Client Side for AWS with graphical Client Project

import json
import sys
import time
import datetime
import matplotlib.pyplot as plt
import boto3
import ast
import decimal
import matplotlib
from PyQt5 import QtCore, QtGui, QtWidgets



class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.textName = QtWidgets.QLineEdit(self)
        self.textPass = QtWidgets.QLineEdit(self)
        self.buttonLogin = QtWidgets.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def handleLogin(self):
        if (self.textName.text() == 'pi' and
            self.textPass.text() == 'maya'):
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Wrong username or password. Try Again!')
            
class Ui_MainWindow(object):
    def __init__(self):
        self.sqs = boto3.resource('sqs')
        # Call the queue by name
        self.queue = self.sqs.get_queue_by_name(QueueName='EIDProject4_Queue')
        self.max_temp_list=[]
        self.min_temp_list=[]
        self.curr_temp_list=[]
        self.avg_temp_list=[]
        self.max_humid_list=[]
        self.min_humid_list=[]
        self.curr_humid_list=[]
        self.avg_humid_list=[]
        self.num_readings = 0
        self.mult_factor = 1.0
        self.add_factor = 0.0
        self.unit = " C\n"

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("EIDProject3-Client")
        MainWindow.resize(1316, 671)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.TempGraph = QtWidgets.QPushButton(self.centralWidget)
        self.TempGraph.setGeometry(QtCore.QRect(250, 400, 200, 90))
        self.TempGraph.setAutoFillBackground(False)
        self.TempGraph.setObjectName("TempGraph")
        self.HumGraph = QtWidgets.QPushButton(self.centralWidget)
        self.HumGraph.setGeometry(QtCore.QRect(500, 400, 200, 90))
        self.HumGraph.setAutoFillBackground(False)
        self.HumGraph.setObjectName("HumGraph")
        self.RequestData = QtWidgets.QPushButton(self.centralWidget)
        self.RequestData.setGeometry(QtCore.QRect(330, 200, 181, 121))
        self.RequestData.setAutoFillBackground(False)
        self.RequestData.setObjectName("RequestData")
        self.FahrenheitToCelcius = QtWidgets.QRadioButton(self.centralWidget)
        self.FahrenheitToCelcius.setGeometry(QtCore.QRect(60, 210, 70, 27))
        self.FahrenheitToCelcius.setObjectName("FahrenheitToCelcius")
        self.CtoFlabel = QtWidgets.QLabel(self.centralWidget)
        self.CtoFlabel.setGeometry(QtCore.QRect(30, 310, 210, 21))
        self.CtoFlabel.setObjectName("CtoFlabel")
        self.CelciusToFahrenhite = QtWidgets.QRadioButton(self.centralWidget)
        self.CelciusToFahrenhite.setGeometry(QtCore.QRect(60, 350, 75, 27))
        self.CelciusToFahrenhite.setObjectName("CelsiusToFahrenheit")
        self.FtoClabel = QtWidgets.QLabel(self.centralWidget)
        self.FtoClabel.setGeometry(QtCore.QRect(30, 180, 210, 21))
        self.FtoClabel.setObjectName("FtoClabel")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(300, 0, 211, 131))
        self.label.setAutoFillBackground(True)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setScaledContents(True)
        self.label.setWordWrap(True)
        self.label.setIndent(35)
        self.label.setObjectName("label")
        # Message Box for displaying data/error messages
        self.MessageBox = QtWidgets.QTextEdit(self.centralWidget)
        self.MessageBox.setGeometry(QtCore.QRect(760, 0, 531, 601))
        self.MessageBox.setObjectName("MessageBox")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(630, 260, 67, 21))
        self.label_2.setObjectName("label_2")
        self.ClearMessage = QtWidgets.QPushButton(self.centralWidget)
        self.ClearMessage.setGeometry(QtCore.QRect(600, 520, 151, 29))
        self.ClearMessage.setObjectName("ClearMessage")
        self.Close = QtWidgets.QPushButton(self.centralWidget)
        self.Close.setGeometry(QtCore.QRect(210, 520, 121, 31))
        self.Close.setObjectName("Close")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1316, 26))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        # Calling appropriate functions on different button clicks
        self.Close.clicked.connect(MainWindow.close)
        self.ClearMessage.clicked.connect(self.MessageBox.clear)
        self.RequestData.clicked.connect(self.fetch_data)
        self.TempGraph.clicked.connect(self.plotGraphTemp)
        self.HumGraph.clicked.connect(self.plotGraphHum)
        self.FahrenheitToCelcius.clicked.connect(self.fah_to_cel)
        self.CelciusToFahrenhite.clicked.connect(self.cel_to_fah)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "EIDProject 3 - Client"))
        self.RequestData.setText(_translate("MainWindow", "Get Data"))
        self.FahrenheitToCelcius.setText(_translate("MainWindow", "F to  C"))
        self.CtoFlabel.setText(_translate("MainWindow", "Change Scale to Fahrenheit"))
        self.CelciusToFahrenhite.setText(_translate("MainWindow", "C to F"))
        self.FtoClabel.setText(_translate("MainWindow", "Change Scale to Celsius"))
        self.label.setText(_translate("MainWindow", "Weather Data"))
        self.label_2.setText(_translate("MainWindow", "Message"))
        self.ClearMessage.setText(_translate("MainWindow", "Clear"))
        self.Close.setText(_translate("MainWindow", "Close"))
        self.TempGraph.setText(_translate("MainWindow","Plot Temp"))
        self.HumGraph.setText(_translate("MainWindow","Plot Hum"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))



    def fetch_data(self):
        # Receive message from SQS queue
        queuelist = []
        for i in range(3):
            offload_list = self.queue.receive_messages(MaxNumberOfMessages=10)
            if not offload_list:
                break
        # Process messages by printing out body
            for msg in offload_list:
                msgbody = ast.literal_eval(msg.body)
                queuelist.append(msgbody)
        # delete the msg
                msg.delete()
                self.num_readings += 1

        # Take out data from individual messages and classify them based on key
        if queuelist:
            for mesg in queuelist:
                self.curr_temp_list.append(mesg["curr_temp"])
                self.curr_humid_list.append(mesg["curr_humid"])
                self.max_temp_list.append(mesg["max_temp"])
                self.max_humid_list.append(mesg["max_humid"])
                self.min_temp_list.append(mesg["min_temp"])
                self.min_humid_list.append(mesg["min_humid"])
                self.avg_temp_list.append(mesg["avg_temp"])
                self.avg_humid_list.append(mesg["avg_humid"])

            # generate message to be printed in Message Box
            final_mesg=""
            for max_t,min_t,curr_t,avg_t,max_h,min_h,curr_h,avg_h in zip(self.max_temp_list,\
                self.min_temp_list,self.curr_temp_list, self.avg_temp_list, self.max_humid_list,\
                self.min_humid_list, self.curr_humid_list, self.avg_humid_list):


                final_mesg +=   "Max Temp: {0:.2f}".format((max_t*self.mult_factor)+self.add_factor) + self.unit + \
                                "Min Temp: {0:.2f}".format((min_t*self.mult_factor)+self.add_factor) + self.unit + \
                                "Last Temp: {0:.2f}".format((curr_t*self.mult_factor)+self.add_factor) + self.unit + \
                                "Avg Temp: {0:.2f}".format((avg_t*self.mult_factor)+self.add_factor) + self.unit + \
                                "Max Hum: "+ str(max_h) + " %\n" + \
                                "Min Hum: "+ str(min_h) + " %\n" + \
                                "Last Hum: "+ str(curr_h) + " %\n" + \
                                "Avg Hum: "+ str(avg_h) + " %\n\n"


            self.MessageBox.setText("Fetched Data:\n"  + final_mesg + "\nTimestamp: " + str(datetime.datetime.now()))
        # Error Handling
        else:
            self.MessageBox.setText("Error Fetching Data \n")


    # Function for plotting graph of humidity and temperature separately
    def plotGraphTemp(self):
        plt.plot(range(self.num_readings), self.max_temp_list, 'b-', label='Max Temp')
        plt.plot(range(self.num_readings), self.min_temp_list, 'r-', label='Min Temp')
        plt.plot(range(self.num_readings), self.curr_temp_list, 'y-', label='Last Temp')
        plt.plot(range(self.num_readings), self.avg_temp_list, 'g-', label='Avg Temp')
        plt.legend(loc='best')
        plt.title('Temperature Plot')
        plt.ylabel('Temperature C')
        plt.xlabel('Count')
        plt.show()

    def plotGraphHum(self):
        plt.plot(range(self.num_readings), self.max_humid_list, 'b-', label='Max Hum')
        plt.plot(range(self.num_readings), self.min_humid_list, 'r-', label='Min Hum')
        plt.plot(range(self.num_readings), self.curr_humid_list, 'y-', label='Last Hum')
        plt.plot(range(self.num_readings), self.avg_humid_list, 'g-', label='Avg Hum')
        plt.legend(loc='best')
        plt.title('Humidity Plot')
        plt.ylabel('Humidity %')
        plt.xlabel('Count')
        plt.show()

    # Unit conversion
    def cel_to_fah(self):
        self.mult_factor = 1.8
        self.add_factor = 32.0
        self.unit = " F\n"


    def fah_to_cel(self):
        self.mult_factor = 1.0
        self.add_factor = 0.0
        self.unit = " C\n"


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    login = Login()
    if login.exec_() == QtWidgets.QDialog.Accepted:
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
