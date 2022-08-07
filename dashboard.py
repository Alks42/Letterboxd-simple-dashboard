from PyQt5 import QtCore, QtGui, QtWidgets, QtChart


class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.resize(1400, 1000)
        self.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)

        self.gridLayoutWidget = QtWidgets.QWidget()
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1400, 1000))
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 20, 10, 0)

        self.setCentralWidget(self.gridLayoutWidget)
        self.statusbar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusbar)

        self.frame_to_call_frame = QtWidgets.QFrame(self.gridLayoutWidget)
        self.frame_to_call_frame.setMinimumWidth(10)

        # Side Frame
        self.side_frame = QtWidgets.QFrame(self.gridLayoutWidget)
        self.side_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.side_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.side_layout = QtWidgets.QVBoxLayout(self.side_frame)
        self.label_top = QtWidgets.QLabel(self.side_frame)
        self.side_button = QtWidgets.QPushButton(self.side_frame)
        self.form = QtWidgets.QLineEdit(self.side_frame)
        self.form.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.checkSave = QtWidgets.QCheckBox(self.side_frame)
        self.checkLock = QtWidgets.QCheckBox(self.side_frame)
        self.label_bottom = QtWidgets.QLabel(self.side_frame)

        self.side_layout.addWidget(self.label_top, 0, QtCore.Qt.AlignTop)
        self.side_layout.addWidget(self.side_button, 0, QtCore.Qt.AlignTop)
        self.side_layout.addWidget(self.form, 0, QtCore.Qt.AlignBottom)
        self.side_layout.addWidget(self.checkSave, 0, QtCore.Qt.AlignBottom)
        self.side_layout.addWidget(self.checkLock, 0, QtCore.Qt.AlignBottom)
        self.side_layout.addWidget(self.label_bottom, 0, QtCore.Qt.AlignBottom)

        # Reviews, comments, Filmtime TotalFilms
        self.Rewievs = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Comments = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Filmtime = QtWidgets.QLabel(self.gridLayoutWidget)

        # geners, country default
        self.GenersBar = QtWidgets.QLabel(self.gridLayoutWidget)
        self.CountriesBar = QtWidgets.QLabel(self.gridLayoutWidget)

        # Rating frame
        self.RatingFrame = QtWidgets.QFrame(self.gridLayoutWidget)
        self.RatingFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.RatingFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ratinglayout = QtWidgets.QHBoxLayout(self.RatingFrame)
        self.AvgRating = QtWidgets.QLabel(self.RatingFrame)

        self.ratinglayout.addWidget(self.create_bar(clean_data.overall[1]))
        self.ratinglayout.addWidget(self.AvgRating)

        # Stacked Widget
        self.stackedWidget = QtWidgets.QStackedWidget(self.gridLayoutWidget)
        self.page = QtWidgets.QWidget()

        self.PieChart = QtChart.QChart()
        self.series = QtChart.QPieSeries()
        self.series.setHoleSize(0.4)
        for key, value in clean_data.overall[5].items():
            self.series.append(str(key), value)
        self.PieChart.addSeries(self.series)
        self.piechart_view = QtChart.QChartView(self.PieChart)
        self.PieChart.setAnimationOptions(QtChart.QChart.SeriesAnimations)
        self.PieChart.legend().setVisible(False)


        self.chartLayout = QtWidgets.QVBoxLayout(self.page)
        self.chartLayout.addWidget(self.piechart_view)

        self.stackedWidget.addWidget(self.page)

        self.page_2 = QtWidgets.QWidget()

        self.Gistogramma = QtWidgets.QLabel(self.page_2)
        self.stackedWidget.addWidget(self.page_2)

        self.stackedWidget.setCurrentIndex(0)

        # Best Frame
        self.BestFrame = QtWidgets.QFrame(self.gridLayoutWidget)
        self.BestFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.BestFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.bestLayout = QtWidgets.QHBoxLayout(self.BestFrame)

        self.BestLabel = QtWidgets.QLabel(self.BestFrame)
        self.BestTable = QtWidgets.QTableView(self.BestFrame)
        self.BestTable.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.bestLayout.addWidget(self.BestLabel)
        self.bestLayout.addWidget(self.BestTable)

        # Worst frame
        self.WorstFrame = QtWidgets.QFrame(self.gridLayoutWidget)
        self.WorstFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.WorstFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.worstLayout = QtWidgets.QHBoxLayout(self.WorstFrame)

        self.worstLabel = QtWidgets.QLabel(self.WorstFrame)
        self.WorsTable = QtWidgets.QTableView(self.WorstFrame)
        self.WorsTable.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.worstLayout.addWidget(self.worstLabel)
        self.worstLayout.addWidget(self.WorsTable)

        self.gridLayout.addWidget(self.frame_to_call_frame, 0, 0, 5, 1)
        self.gridLayout.addWidget(self.side_frame, 0, 1, 5, 1)
        self.gridLayout.addWidget(self.stackedWidget, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.Filmtime, 1, 3, 1, 1)
        if clean_data.overall[-1]:
            self.GenersBar = self.create_bar(clean_data.overall[-1][0], True)
            self.CountriesBar = self.create_bar(clean_data.overall[-1][1], True)
        self.gridLayout.addWidget(self.CountriesBar, 0, 4, 2, 1)
        self.gridLayout.addWidget(self.GenersBar, 0, 2, 2, 1)
        self.gridLayout.addWidget(self.Rewievs, 2, 4, 1, 1)
        self.gridLayout.addWidget(self.Comments, 2, 2, 1, 1)
        self.gridLayout.addWidget(self.RatingFrame, 2, 3, 1, 1)
        self.gridLayout.addWidget(self.BestFrame, 3, 2, 1, 3)
        self.gridLayout.addWidget(self.WorstFrame, 4, 2, 1, 3)

        self.side_frame.installEventFilter(self)
        self.side_frame.hide()
        self.frame_to_call_frame.installEventFilter(self)

        self.setupUi()


    def setupUi(self):
        self.label_top.setText('Experimental')
        self.label_bottom.setText('Experimental')
        self.side_button.setText('2089')
        self.form.setText('Experimental')
        self.checkSave.setText('Save')
        self.checkLock.setText('Lock Side Menu')

        self.Comments.setText('Comments')
        self.Rewievs.setText('Rewievs')
        # self.PieChart.setText('PieChart')
        self.Gistogramma.setText('Gistogramma')
        # self.RatingChart.setText('RatingChart')
        self.AvgRating.setText('AvgRating')
        self.BestLabel.setText('Experimental')
        self.worstLabel.setText('Experimental')
        self.Filmtime.setText('filmTime')

    def create_bar(self, df, isvertical=False):
        self.barchart = QtChart.QChart()
        self.barset = QtChart.QBarSet('rate')
        self.axis = QtChart.QBarCategoryAxis()

        if not isvertical:
            self.bar_series = QtChart.QBarSeries()
            bar_data = df
            self.barchart.setAxisX(self.axis)
        else:
            self.bar_series = QtChart.QHorizontalBarSeries()
            bar_data = dict(sorted(df.items(), key=lambda item: item[1]))
            self.barchart.setAxisY(self.axis)

        self.axis.append(str(k) for k in bar_data.keys())
        for value in bar_data.values():
            self.barset.append(value)
        self.bar_series.append(self.barset)
        self.barchart.addSeries(self.bar_series)
        self.chart_view = QtChart.QChartView(self.barchart)
        self.barchart.setAnimationOptions(QtChart.QChart.SeriesAnimations)
        self.barchart.legend().setVisible(False)
        return self.chart_view

    def eventFilter(self, obj, event):
        if obj is self.frame_to_call_frame and event.type() == QtCore.QEvent.Enter:
            self.frame_to_call_frame.hide()
            self.side_frame.show()
            return True
        elif obj is self.side_frame and event.type() == QtCore.QEvent.Leave and  self.checkLock.checkState() == 0:
            self.side_frame.hide()
            self.frame_to_call_frame.show()
            return True
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    import sys
    import clean_data

    print(clean_data.overall)
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())

