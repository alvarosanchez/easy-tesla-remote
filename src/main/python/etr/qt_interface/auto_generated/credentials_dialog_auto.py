# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'credentials_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CredentialsDialog(object):
    def setupUi(self, CredentialsDialog):
        CredentialsDialog.setObjectName("CredentialsDialog")
        CredentialsDialog.resize(442, 242)
        self.verticalLayout = QtWidgets.QVBoxLayout(CredentialsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Token = QtWidgets.QTabWidget(CredentialsDialog)
        self.Token.setObjectName("Token")
        self.tabUser = QtWidgets.QWidget()
        self.tabUser.setObjectName("tabUser")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tabUser)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.tabUser)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.userName = QtWidgets.QLineEdit(self.tabUser)
        self.userName.setReadOnly(False)
        self.userName.setObjectName("userName")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.userName)
        self.label_2 = QtWidgets.QLabel(self.tabUser)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.userPassword = QtWidgets.QLineEdit(self.tabUser)
        self.userPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.userPassword.setObjectName("userPassword")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.userPassword)
        self.message = QtWidgets.QLabel(self.tabUser)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.message.setFont(font)
        self.message.setText("")
        self.message.setObjectName("message")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.message)
        self.verticalLayout_3.addLayout(self.formLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.Token.addTab(self.tabUser, "")
        self.tabToken = QtWidgets.QWidget()
        self.tabToken.setObjectName("tabToken")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tabToken)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_4 = QtWidgets.QLabel(self.tabToken)
        self.label_4.setObjectName("label_4")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.apiToken = QtWidgets.QLineEdit(self.tabToken)
        self.apiToken.setObjectName("apiToken")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.apiToken)
        self.TokenMessage = QtWidgets.QLabel(self.tabToken)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.TokenMessage.setFont(font)
        self.TokenMessage.setText("")
        self.TokenMessage.setObjectName("TokenMessage")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.TokenMessage)
        self.verticalLayout_4.addLayout(self.formLayout_3)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.Token.addTab(self.tabToken, "")
        self.verticalLayout_2.addWidget(self.Token)
        self.label_5 = QtWidgets.QLabel(CredentialsDialog)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.DemoMode = QtWidgets.QPushButton(CredentialsDialog)
        self.DemoMode.setObjectName("DemoMode")
        self.horizontalLayout_2.addWidget(self.DemoMode)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.buttonBox = QtWidgets.QDialogButtonBox(CredentialsDialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_2.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(CredentialsDialog)
        self.Token.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(CredentialsDialog)

    def retranslateUi(self, CredentialsDialog):
        _translate = QtCore.QCoreApplication.translate
        CredentialsDialog.setWindowTitle(_translate("CredentialsDialog", "Account Credentials"))
        self.label.setText(_translate("CredentialsDialog", "User"))
        self.label_2.setText(_translate("CredentialsDialog", "Password"))
        self.Token.setTabText(self.Token.indexOf(self.tabUser), _translate("CredentialsDialog", "User and password"))
        self.label_4.setText(_translate("CredentialsDialog", "Token:"))
        self.Token.setTabText(self.Token.indexOf(self.tabToken), _translate("CredentialsDialog", "Token"))
        self.label_5.setText(_translate("CredentialsDialog", "If you don\'t have a Tesla account click the button to enter demo mode"))
        self.DemoMode.setText(_translate("CredentialsDialog", "Demo mode"))


