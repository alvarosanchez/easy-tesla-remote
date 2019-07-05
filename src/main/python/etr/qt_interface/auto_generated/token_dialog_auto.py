# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'token_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TokenDialog(object):
    def setupUi(self, TokenDialog):
        TokenDialog.setObjectName("TokenDialog")
        TokenDialog.resize(379, 176)
        self.verticalLayout = QtWidgets.QVBoxLayout(TokenDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(TokenDialog)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.tokenBox = QtWidgets.QPlainTextEdit(TokenDialog)
        self.tokenBox.setReadOnly(True)
        self.tokenBox.setObjectName("tokenBox")
        self.verticalLayout_2.addWidget(self.tokenBox)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(TokenDialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(TokenDialog)
        QtCore.QMetaObject.connectSlotsByName(TokenDialog)

    def retranslateUi(self, TokenDialog):
        _translate = QtCore.QCoreApplication.translate
        TokenDialog.setWindowTitle(_translate("TokenDialog", "Account token"))
        self.label.setText(_translate("TokenDialog", "Current token:"))


