# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(350, 196)
        self.verticalLayout = QtWidgets.QVBoxLayout(AboutDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(AboutDialog)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtWidgets.QLabel(AboutDialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.uiVersion = QtWidgets.QLabel(AboutDialog)
        self.uiVersion.setObjectName("uiVersion")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.uiVersion)
        self.label_2 = QtWidgets.QLabel(AboutDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.engineVersion = QtWidgets.QLabel(AboutDialog)
        self.engineVersion.setObjectName("engineVersion")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.engineVersion)
        self.verticalLayout_2.addLayout(self.formLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.label_6 = QtWidgets.QLabel(AboutDialog)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setOpenExternalLinks(True)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.licenseButton = QtWidgets.QPushButton(AboutDialog)
        self.licenseButton.setObjectName("licenseButton")
        self.horizontalLayout.addWidget(self.licenseButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.closeButton = QtWidgets.QPushButton(AboutDialog)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(AboutDialog)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        _translate = QtCore.QCoreApplication.translate
        AboutDialog.setWindowTitle(_translate("AboutDialog", "About"))
        self.label.setText(_translate("AboutDialog", "Easy Tesla Remote"))
        self.label_3.setText(_translate("AboutDialog", "QT UI Version:"))
        self.uiVersion.setText(_translate("AboutDialog", "uiVersion"))
        self.label_2.setText(_translate("AboutDialog", "Engine Version:"))
        self.engineVersion.setText(_translate("AboutDialog", "engineVersion"))
        self.label_6.setText(_translate("AboutDialog", "<a href=\"https://github.com/jumimo/easy-tesla-remote\">Easy Tesla Remote on Github</a>"))
        self.licenseButton.setText(_translate("AboutDialog", "License"))
        self.closeButton.setText(_translate("AboutDialog", "Close"))


