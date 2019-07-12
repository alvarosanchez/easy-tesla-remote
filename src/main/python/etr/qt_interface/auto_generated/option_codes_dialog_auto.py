# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'option_codes_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_OptionsCodeDialog(object):
    def setupUi(self, OptionsCodeDialog):
        OptionsCodeDialog.setObjectName("OptionsCodeDialog")
        OptionsCodeDialog.resize(722, 333)
        self.verticalLayout = QtWidgets.QVBoxLayout(OptionsCodeDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(OptionsCodeDialog)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.optionCodes = QtWidgets.QPlainTextEdit(OptionsCodeDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.optionCodes.sizePolicy().hasHeightForWidth())
        self.optionCodes.setSizePolicy(sizePolicy)
        self.optionCodes.setMinimumSize(QtCore.QSize(0, 50))
        self.optionCodes.setReadOnly(False)
        self.optionCodes.setObjectName("optionCodes")
        self.verticalLayout_2.addWidget(self.optionCodes)
        self.codeTable = QtWidgets.QTableView(OptionsCodeDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.codeTable.sizePolicy().hasHeightForWidth())
        self.codeTable.setSizePolicy(sizePolicy)
        self.codeTable.setObjectName("codeTable")
        self.codeTable.horizontalHeader().setVisible(False)
        self.codeTable.horizontalHeader().setStretchLastSection(True)
        self.codeTable.verticalHeader().setVisible(False)
        self.verticalLayout_2.addWidget(self.codeTable)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.message = QtWidgets.QLabel(OptionsCodeDialog)
        self.message.setText("")
        self.message.setObjectName("message")
        self.horizontalLayout.addWidget(self.message)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.translateCodes = QtWidgets.QPushButton(OptionsCodeDialog)
        self.translateCodes.setObjectName("translateCodes")
        self.horizontalLayout.addWidget(self.translateCodes)
        self.closeDialog = QtWidgets.QPushButton(OptionsCodeDialog)
        self.closeDialog.setObjectName("closeDialog")
        self.horizontalLayout.addWidget(self.closeDialog)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(OptionsCodeDialog)
        QtCore.QMetaObject.connectSlotsByName(OptionsCodeDialog)

    def retranslateUi(self, OptionsCodeDialog):
        _translate = QtCore.QCoreApplication.translate
        OptionsCodeDialog.setWindowTitle(_translate("OptionsCodeDialog", "Option Code Translator"))
        self.label.setText(_translate("OptionsCodeDialog", "Option codes (separate multiple codes using commas):"))
        self.translateCodes.setText(_translate("OptionsCodeDialog", "Translate"))
        self.closeDialog.setText(_translate("OptionsCodeDialog", "Close"))


