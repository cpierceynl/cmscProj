#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QFormLayout,    QApplication, QLineEdit, QLabel, QWidget, QPushButton, QComboBox,    QRadioButton
import sys


# In[2]:


class inputScreen(QMainWindow):
    """
    Take input from user to define analysis.
    """
    def __init__(self, parent=None):
        super(inputScreen, self).__init__(parent)
        self.layout = QFormLayout()  # set layout as form
        self.screen = QWidget()  # initialize widget
        
        # create list of possible latitude and longitude values to populate
        # QComboBox
        # using QComboBox to avoid user entry errors
        lons = list(np.arange(0.5, 360, 0.5))
        lons = [str(i) for i in lons]
        lats = list(np.arange(65.5, 90, 0.5))
        lats = [str(i) for i in lats]
        years = list(np.arange(1950, 2022, 1))
        years = [str(i) for i in years]
        months = list(np.arange(1, 13, 1))
        months = [str(i) for i in months]
        years_fut = list(np.arange(2023, 2035, 1))
        years_fut = [str(i) for i in years_fut]
        
        #  create labels to assign to input fields
        lat_label_start = QLabel("Latitude: ")
        lon_label_start = QLabel("Longitude: ")
        
        # create submit button
        submit_inputs = QPushButton("Run analysis...")

        # populate QComboBox
        self.lat_input_start = QComboBox()
        self.lon_input_start = QComboBox()
        self.lat_input_start.addItems(lats)
        self.lon_input_start.addItems(lons)
        
        # options for seeing ice concentration or predicting
        self.prev_conc = QRadioButton("See ice concentration for...")
        yearlbl1 = QLabel("year: ")
        monthlbl1 = QLabel("month: ")
        self.yearinput1 = QComboBox()
        self.monthinput1 = QComboBox()
        self.yearinput1.addItems(years)
        self.monthinput1.addItems(months)
        self.predict_conc = QRadioButton("Predict concentration for...")
        yearlbl2 = QLabel("year: ")
        monthlbl2 = QLabel("month: ")
        self.yearinput2 = QComboBox()
        self.monthinput2 = QComboBox()
        self.yearinput2.addItems(years_fut)
        self.monthinput2.addItems(months)

        # add dropdown boxes to form
        self.layout.addRow(lat_label_start, self.lat_input_start)
        self.layout.addRow(lon_label_start, self.lon_input_start)
        self.layout.addRow(self.prev_conc)
        self.layout.addRow(yearlbl1, self.yearinput1)
        self.layout.addRow(monthlbl1, self.monthinput1)
        self.layout.addRow(self.predict_conc)
        self.layout.addRow(yearlbl2, self.yearinput2)
        self.layout.addRow(monthlbl2, self.monthinput2)
        
        # add buttom to form
        self.layout.addRow(submit_inputs)

        # set the layout to the screen and set screen as central widget
        self.screen.setLayout(self.layout)
        self.setCentralWidget(self.screen)

        # when button pressed, call manage_inputs to check and make next calls
        submit_inputs.pressed.connect(self.manage_inputs)

    def manage_inputs(self):
        """
        check and handle inputs
        """
        #  convert to float values
        start_lat = float(self.lat_input_start.currentText())
        start_lon = float(self.lon_input_start.currentText())
        
        if self.prev_conc.isChecked():
            month = float(self.monthinput1.currentText())
            year = float(self.yearinput1.currentText())
            analysis = 1  # label which analysis to run
        elif self.predict_conc.isChecked():
            month = float(self.monthinput2.currentText())
            year = float(self.yearinput2.currentText())
            analysis = 2

        path = grabData(start_lat, start_lon, month, year, analysis)


# In[3]:


def main():
    app = QApplication(sys.argv)
    win = inputScreen()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


# In[ ]:




