# -*- coding: utf-8 -*-

import  qgis.core
import sys
from PyQt5.QtGui import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from qgis.core import *
from qgis.gui import *
from qgis.utils import *

import database
from unittest import TestCase

class DummyInterface(object):
    def __getattr__(self, *args, **kwargs):
        def dummy(*args, **kwargs):
            return self
        return dummy
    def __iter__(self):
        return self
    def next(self):
        raise StopIteration
    def layers(self):
        # simulate iface.legendInterface().layers()
        return QgsProject.instance().mapLayers().values()

iface = DummyInterface()

class TestDatabase(TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)

        # create gui
        self.form = database.Database(iface)
        self.ui = self.form.joinDB_dlg

    # test default values
    def test_defaults(self):
        self.assertEqual(self.ui.lineEdit_address.text(), "10.1.1.4")
        self.assertEqual(self.ui.lineEdit_dbname.text(), "gis")
        self.assertEqual(self.ui.lineEdit_user.text(), "wing")
        self.assertEqual(self.ui.lineEdit_password.text(), "")
        self.assertEqual(self.ui.textEdit_sql.toPlainText(), "SELECT * from public.typy_vykopu")

        values = [(1, 'Výkop - prostý terén - trávník, zeleň', 0),
                  (2, 'Podvrt - průjezd, chodník, vjezd', 0),
                  (3, 'Protlak', 0),
                  (4, 'Překop - kostky', 0),
                  (5, 'Překop - asfalt', 0),
                  (6, 'Překop -polní cesta', 0),
                  (7, 'Výkop chodník - stará dlažba', 0),
                  (8, 'Výkop chodník - zámková dlažba nová', 0),
                  (9, 'Výkop chodník - kostky', 0)]

        for row in range(self.ui.tableWidget.rowCount()):
            self.assertEqual(self.ui.tableWidget.item(row, 0).text(), str(values[row][0]))
            self.assertEqual(self.ui.tableWidget.item(row, 1).text(), values[row][1])
            self.assertEqual(self.ui.tableWidget.item(row, 2).text(), str(values[row][2]))

    # test dialog name
    def test_dlg_name(self):
        self.assertEqual(self.ui.windowTitle(), 'Connect to Database')

    # test not empty table values
    def test_not_epmpty_widget_table(self):
        for row in range(self.ui.tableWidget.rowCount()):
            self.assertNotEqual(self.ui.tableWidget.item(row, 0).text(), "")
            self.assertNotEqual(self.ui.tableWidget.item(row, 1).text(), "")
            self.assertNotEqual(self.ui.tableWidget.item(row, 2).text(), "")

    # test not empty values
    def test_connect_to_db(self):
        self.ui.pushButton_connect.click()
        self.assertNotEqual(self.ui.lineEdit_address.text(), "")
        self.assertNotEqual(self.ui.lineEdit_dbname.text(), "")
        self.assertNotEqual(self.ui.lineEdit_user.text(), "")
        self.assertNotEqual(self.ui.textEdit_sql.toPlainText(), "")

        self.assertEqual(self.ui.lineEdit_address.text(), "10.1.1.4")
        self.assertEqual(self.ui.lineEdit_dbname.text(), "gis")
        self.assertEqual(self.ui.lineEdit_user.text(), "wing")
        self.assertEqual(self.ui.lineEdit_password.text(), "")
        self.assertEqual(self.ui.textEdit_sql.toPlainText(), "SELECT * from public.typy_vykopu")

        for row in range(self.ui.tableWidget.rowCount()):
            self.assertNotEqual(self.ui.tableWidget.item(row, 0).text(), 0)
            self.assertNotEqual(self.ui.tableWidget.item(row, 1).text(), 0)
            self.assertNotEqual(self.ui.tableWidget.item(row, 2).text(), 0)

    # test standard values
    def test_fill_standard_values(self):
        values = [(1, 'Výkop - prostý terén - trávník, zeleň', 100.00),
                  (2, 'Podvrt - průjezd, chodník, vjezd', 200.00),
                  (3, 'Protlak', 700.00),
                  (4, 'Překop - kostky', 540.00),
                  (5, 'Překop - asfalt', 633.00),
                  (6, 'Překop -polní cesta', 200.00),
                  (7, 'Výkop chodník - stará dlažba', 193.00),
                  (8, 'Výkop chodník - zámková dlažba nová', 216.00),
                  (9, 'Výkop chodník - kostky', 540.00)]

        self.ui.pushButton_standard.click()
        for row in range(self.ui.tableWidget.rowCount()):
            self.assertEqual(self.ui.tableWidget.item(row, 0).text(), str(values[row][0]))
            self.assertEqual(self.ui.tableWidget.item(row, 1).text(), values[row][1])
            self.assertEqual(self.ui.tableWidget.item(row, 2).text(), str(values[row][2]))

    # test OK button close dialog
    def test_click_widget(self):
        self.ui.show()
        self.assertEqual(self.ui.isVisible(), True)
        okWidget = self.ui.button_box.button(self.ui.button_box.Ok)
        QTest.mouseClick(okWidget, Qt.LeftButton)
        self.assertEqual(self.ui.isVisible(), False)