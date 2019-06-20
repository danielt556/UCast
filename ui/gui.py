# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1077, 485)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/images/transparent earth  icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setAutoFillBackground(True)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setContentsMargins(0, 0, -1, -1)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.PredictLayout = QtWidgets.QVBoxLayout()
        self.PredictLayout.setObjectName("PredictLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.PredictLayout.addItem(spacerItem)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.PredictLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.txtTrainTimestamps = QtWidgets.QLineEdit(self.centralwidget)
        self.txtTrainTimestamps.setMinimumSize(QtCore.QSize(0, 0))
        self.txtTrainTimestamps.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.txtTrainTimestamps.setObjectName("txtTrainTimestamps")
        self.horizontalLayout.addWidget(self.txtTrainTimestamps)
        self.PredictLayout.addLayout(self.horizontalLayout)
        self.trainLayout = QtWidgets.QVBoxLayout()
        self.trainLayout.setObjectName("trainLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btnTrain = QtWidgets.QPushButton(self.centralwidget)
        self.btnTrain.setMaximumSize(QtCore.QSize(85, 25))
        self.btnTrain.setObjectName("btnTrain")
        self.horizontalLayout_3.addWidget(self.btnTrain)
        self.btnLoadModel = QtWidgets.QPushButton(self.centralwidget)
        self.btnLoadModel.setMaximumSize(QtCore.QSize(85, 25))
        self.btnLoadModel.setObjectName("btnLoadModel")
        self.horizontalLayout_3.addWidget(self.btnLoadModel)
        self.btnSaveModel = QtWidgets.QPushButton(self.centralwidget)
        self.btnSaveModel.setMaximumSize(QtCore.QSize(85, 25))
        self.btnSaveModel.setObjectName("btnSaveModel")
        self.horizontalLayout_3.addWidget(self.btnSaveModel)
        self.trainLayout.addLayout(self.horizontalLayout_3)
        self.PredictLayout.addLayout(self.trainLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.PredictLayout.addItem(spacerItem1)
        self.gridLayout_5.addLayout(self.PredictLayout, 4, 0, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.gridLayout_4.setContentsMargins(0, -1, -1, -1)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setMinimumSize(QtCore.QSize(400, 60))
        self.groupBox.setMaximumSize(QtCore.QSize(400, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.cbBefore = QtWidgets.QCheckBox(self.groupBox)
        self.cbBefore.setGeometry(QtCore.QRect(10, 30, 132, 18))
        self.cbBefore.setObjectName("cbBefore")
        self.cbIgnore = QtWidgets.QCheckBox(self.groupBox)
        self.cbIgnore.setGeometry(QtCore.QRect(140, 30, 132, 18))
        self.cbIgnore.setObjectName("cbIgnore")
        self.cbAfter = QtWidgets.QCheckBox(self.groupBox)
        self.cbAfter.setGeometry(QtCore.QRect(290, 30, 100, 18))
        self.cbAfter.setObjectName("cbAfter")
        self.gridLayout_2.addWidget(self.groupBox, 1, 0, 1, 1)
        self.ddFeature = QtWidgets.QComboBox(self.centralwidget)
        self.ddFeature.setObjectName("ddFeature")
        self.ddFeature.addItem("")
        self.ddFeature.addItem("")
        self.ddFeature.addItem("")
        self.gridLayout_2.addWidget(self.ddFeature, 0, 0, 1, 1)
        self.gbFeatures = QtWidgets.QGroupBox(self.centralwidget)
        self.gbFeatures.setEnabled(True)
        self.gbFeatures.setMinimumSize(QtCore.QSize(0, 120))
        self.gbFeatures.setMaximumSize(QtCore.QSize(400, 16777215))
        self.gbFeatures.setObjectName("gbFeatures")
        self.cbLevel1 = QtWidgets.QCheckBox(self.gbFeatures)
        self.cbLevel1.setEnabled(True)
        self.cbLevel1.setGeometry(QtCore.QRect(120, 30, 76, 18))
        self.cbLevel1.setObjectName("cbLevel1")
        self.cbLevel2 = QtWidgets.QCheckBox(self.gbFeatures)
        self.cbLevel2.setGeometry(QtCore.QRect(120, 60, 76, 18))
        self.cbLevel2.setObjectName("cbLevel2")
        self.cbLevel3 = QtWidgets.QCheckBox(self.gbFeatures)
        self.cbLevel3.setGeometry(QtCore.QRect(120, 90, 76, 18))
        self.cbLevel3.setObjectName("cbLevel3")
        self.cbLevel4 = QtWidgets.QCheckBox(self.gbFeatures)
        self.cbLevel4.setGeometry(QtCore.QRect(220, 30, 76, 18))
        self.cbLevel4.setObjectName("cbLevel4")
        self.cbLevel6 = QtWidgets.QCheckBox(self.gbFeatures)
        self.cbLevel6.setGeometry(QtCore.QRect(220, 60, 76, 18))
        self.cbLevel6.setObjectName("cbLevel6")
        self.cbLevel7 = QtWidgets.QCheckBox(self.gbFeatures)
        self.cbLevel7.setGeometry(QtCore.QRect(220, 90, 76, 18))
        self.cbLevel7.setObjectName("cbLevel7")
        self.cbSelectAll = QtWidgets.QCheckBox(self.gbFeatures)
        self.cbSelectAll.setGeometry(QtCore.QRect(20, 60, 76, 18))
        self.cbSelectAll.setObjectName("cbSelectAll")
        self.gridLayout_2.addWidget(self.gbFeatures, 2, 0, 2, 1)
        self.gridLayout_4.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 1, 1, 3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btnPlot = QtWidgets.QPushButton(self.centralwidget)
        self.btnPlot.setMaximumSize(QtCore.QSize(125, 25))
        self.btnPlot.setObjectName("btnPlot")
        self.horizontalLayout_4.addWidget(self.btnPlot)
        self.gridLayout_5.addLayout(self.horizontalLayout_4, 2, 1, 1, 2)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.gridLayout_6.addItem(spacerItem2, 6, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnPredict = QtWidgets.QPushButton(self.centralwidget)
        self.btnPredict.setMaximumSize(QtCore.QSize(85, 25))
        self.btnPredict.setObjectName("btnPredict")
        self.horizontalLayout_2.addWidget(self.btnPredict)
        self.btnComputeError = QtWidgets.QPushButton(self.centralwidget)
        self.btnComputeError.setMaximumSize(QtCore.QSize(90, 25))
        self.btnComputeError.setObjectName("btnComputeError")
        self.horizontalLayout_2.addWidget(self.btnComputeError)
        self.gridLayout_6.addLayout(self.horizontalLayout_2, 5, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem3, 0, 0, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.txtPredictTimestamps = QtWidgets.QLineEdit(self.centralwidget)
        self.txtPredictTimestamps.setMinimumSize(QtCore.QSize(0, 0))
        self.txtPredictTimestamps.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.txtPredictTimestamps.setAlignment(QtCore.Qt.AlignCenter)
        self.txtPredictTimestamps.setObjectName("txtPredictTimestamps")
        self.horizontalLayout_6.addWidget(self.txtPredictTimestamps)
        self.gridLayout_6.addLayout(self.horizontalLayout_6, 1, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_6, 4, 1, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableFiles = QtWidgets.QTableWidget(self.centralwidget)
        self.tableFiles.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableFiles.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableFiles.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableFiles.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableFiles.setRowCount(0)
        self.tableFiles.setObjectName("tableFiles")
        self.tableFiles.setColumnCount(8)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableFiles.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableFiles.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableFiles.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableFiles.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableFiles.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableFiles.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableFiles.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableFiles.setHorizontalHeaderItem(7, item)
        self.tableFiles.horizontalHeader().setVisible(True)
        self.tableFiles.horizontalHeader().setDefaultSectionSize(80)
        self.tableFiles.horizontalHeader().setHighlightSections(True)
        self.verticalLayout.addWidget(self.tableFiles)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setEnabled(True)
        self.progressBar.setMaximum(100)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.gridLayout_5.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.btnSaveClean = QtWidgets.QPushButton(self.centralwidget)
        self.btnSaveClean.setMaximumSize(QtCore.QSize(85, 25))
        self.btnSaveClean.setObjectName("btnSaveClean")
        self.gridLayout_3.addWidget(self.btnSaveClean, 0, 1, 1, 1)
        self.btnLoadDay = QtWidgets.QPushButton(self.centralwidget)
        self.btnLoadDay.setMaximumSize(QtCore.QSize(85, 25))
        self.btnLoadDay.setCheckable(False)
        self.btnLoadDay.setAutoDefault(False)
        self.btnLoadDay.setDefault(False)
        self.btnLoadDay.setFlat(False)
        self.btnLoadDay.setObjectName("btnLoadDay")
        self.gridLayout_3.addWidget(self.btnLoadDay, 0, 0, 1, 1)
        self.btnClean = QtWidgets.QPushButton(self.centralwidget)
        self.btnClean.setMaximumSize(QtCore.QSize(85, 25))
        self.btnClean.setObjectName("btnClean")
        self.gridLayout_3.addWidget(self.btnClean, 0, 2, 1, 1)
        self.btnUnload = QtWidgets.QPushButton(self.centralwidget)
        self.btnUnload.setMaximumSize(QtCore.QSize(85, 25))
        self.btnUnload.setObjectName("btnUnload")
        self.gridLayout_3.addWidget(self.btnUnload, 0, 3, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_3, 2, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_5, 8, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1077, 23))
        self.menubar.setObjectName("menubar")
        self.menuNOAA = QtWidgets.QMenu(self.menubar)
        self.menuNOAA.setObjectName("menuNOAA")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.menuStart_NOAA = QtWidgets.QAction(MainWindow)
        self.menuStart_NOAA.setObjectName("menuStart_NOAA")
        self.actionSave_Model = QtWidgets.QAction(MainWindow)
        self.actionSave_Model.setObjectName("actionSave_Model")
        self.actionLoad_Model = QtWidgets.QAction(MainWindow)
        self.actionLoad_Model.setObjectName("actionLoad_Model")
        self.actionLoad_Day = QtWidgets.QAction(MainWindow)
        self.actionLoad_Day.setObjectName("actionLoad_Day")
        self.actionSave_Day = QtWidgets.QAction(MainWindow)
        self.actionSave_Day.setObjectName("actionSave_Day")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.menuNOAA.addAction(self.menuStart_NOAA)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave_Model)
        self.menuFile.addAction(self.actionLoad_Model)
        self.menuFile.addAction(self.actionSave_Day)
        self.menuFile.addAction(self.actionLoad_Day)
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuNOAA.menuAction())

        self.retranslateUi(MainWindow)
        self.cbSelectAll.toggled['bool'].connect(self.cbLevel2.setChecked)
        self.cbSelectAll.toggled['bool'].connect(self.cbLevel4.setChecked)
        self.cbSelectAll.toggled['bool'].connect(self.cbLevel1.setChecked)
        self.cbSelectAll.toggled['bool'].connect(self.cbLevel3.setChecked)
        self.cbSelectAll.toggled['bool'].connect(self.cbLevel6.setChecked)
        self.cbSelectAll.toggled['bool'].connect(self.cbLevel7.setChecked)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "UCast"))
        self.txtTrainTimestamps.setPlaceholderText(_translate("MainWindow", "Train Timestamps"))
        self.btnTrain.setText(_translate("MainWindow", "Train"))
        self.btnLoadModel.setText(_translate("MainWindow", "Load Model"))
        self.btnSaveModel.setText(_translate("MainWindow", "Save Model"))
        self.groupBox.setTitle(_translate("MainWindow", "GroupBox"))
        self.cbBefore.setText(_translate("MainWindow", "Before cleaning"))
        self.cbIgnore.setText(_translate("MainWindow", "Ignore invalid values"))
        self.cbAfter.setText(_translate("MainWindow", "After Cleaning"))
        self.ddFeature.setCurrentText(_translate("MainWindow", "R"))
        self.ddFeature.setItemText(0, _translate("MainWindow", "R"))
        self.ddFeature.setItemText(1, _translate("MainWindow", "V"))
        self.ddFeature.setItemText(2, _translate("MainWindow", "VIL"))
        self.gbFeatures.setTitle(_translate("MainWindow", "Features"))
        self.cbLevel1.setText(_translate("MainWindow", "Level 01"))
        self.cbLevel2.setText(_translate("MainWindow", "Level 02"))
        self.cbLevel3.setText(_translate("MainWindow", "Level 03"))
        self.cbLevel4.setText(_translate("MainWindow", "Level 04"))
        self.cbLevel6.setText(_translate("MainWindow", "Level 06"))
        self.cbLevel7.setText(_translate("MainWindow", "Level 07"))
        self.cbSelectAll.setText(_translate("MainWindow", "Select all"))
        self.btnPlot.setText(_translate("MainWindow", "Plot"))
        self.btnPredict.setText(_translate("MainWindow", "Predict"))
        self.btnComputeError.setText(_translate("MainWindow", "Compute Error"))
        self.txtPredictTimestamps.setPlaceholderText(_translate("MainWindow", "Predict Timestamps"))
        item = self.tableFiles.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Date"))
        item = self.tableFiles.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Loaded"))
        item = self.tableFiles.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Clean"))
        item = self.tableFiles.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Timestamps"))
        item = self.tableFiles.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "x"))
        item = self.tableFiles.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "y"))
        item = self.tableFiles.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Features"))
        item = self.tableFiles.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Extention"))
        self.btnSaveClean.setText(_translate("MainWindow", "Save day"))
        self.btnLoadDay.setText(_translate("MainWindow", "Load day"))
        self.btnClean.setText(_translate("MainWindow", "Clean"))
        self.btnUnload.setText(_translate("MainWindow", "Unload"))
        self.menuNOAA.setTitle(_translate("MainWindow", "NOAA"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuStart_NOAA.setText(_translate("MainWindow", "Start NOAA"))
        self.actionSave_Model.setText(_translate("MainWindow", "Save Model"))
        self.actionLoad_Model.setText(_translate("MainWindow", "Load Model"))
        self.actionLoad_Day.setText(_translate("MainWindow", "Load Day"))
        self.actionSave_Day.setText(_translate("MainWindow", "Save Day"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))


from resources import images_rc
