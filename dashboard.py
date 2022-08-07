from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.resize(1100, 800)
        self.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)

        self.gridLayoutWidget = QtWidgets.QWidget()
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1100, 800))
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 10, 0)

        self.setCentralWidget(self.gridLayoutWidget)
        self.statusbar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusbar)

        # Side Frame
        self.side_frame = QtWidgets.QFrame(self.gridLayoutWidget)
        self.side_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.side_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.side_layout = QtWidgets.QVBoxLayout(self.side_frame)
        self.label_top = QtWidgets.QLabel(self.side_frame)
        self.side_button = QtWidgets.QPushButton(self.side_frame)
        self.label_bottom = QtWidgets.QLabel(self.side_frame)

        self.side_layout.addWidget(self.label_top, 0, QtCore.Qt.AlignTop)
        self.side_layout.addWidget(self.side_button, 0, QtCore.Qt.AlignTop)
        self.side_layout.addWidget(self.label_bottom, 0, QtCore.Qt.AlignBottom)

        # Countries, Geners, reviews, comments, Filmtime
        self.CountriesBar = QtWidgets.QLabel(self.gridLayoutWidget)
        self.GenersBar = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Rewievs = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Comments = QtWidgets.QLabel(self.gridLayoutWidget)
        self.Filmtime = QtWidgets.QLabel(self.gridLayoutWidget)


        # Rating graph
        self.RatingFrame = QtWidgets.QFrame(self.gridLayoutWidget)
        self.RatingFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.RatingFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ratinglayout = QtWidgets.QHBoxLayout(self.RatingFrame)

        self.RatingChart = QtWidgets.QLabel(self.RatingFrame)
        self.AvgRating = QtWidgets.QLabel(self.RatingFrame)
        self.ratinglayout.addWidget(self.RatingChart)
        self.ratinglayout.addWidget(self.AvgRating)

        # Stacked Widget
        self.stackedWidget = QtWidgets.QStackedWidget(self.gridLayoutWidget)
        self.page = QtWidgets.QWidget()
        self.verticalLayout_1 = QtWidgets.QVBoxLayout(self.page)

        self.PieChart = QtWidgets.QLabel(self.page)
        self.TotalFilms = QtWidgets.QLabel(self.page)
        self.verticalLayout_1.addWidget(self.PieChart)
        self.verticalLayout_1.addWidget(self.TotalFilms)

        self.stackedWidget.addWidget(self.page)

        self.page_2 = QtWidgets.QWidget()
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.page_2)

        self.TotalFilms2 = QtWidgets.QLabel(self.page_2)
        self.Gistogramma = QtWidgets.QLabel(self.page_2)
        self.verticalLayout_2.addWidget(self.TotalFilms2)
        self.verticalLayout_2.addWidget(self.Gistogramma)

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

        self.gridLayout.addWidget(self.side_frame, 0, 0, 6, 1)
        self.gridLayout.addWidget(self.CountriesBar, 0, 4, 2, 1)
        self.gridLayout.addWidget(self.GenersBar, 0, 1, 2, 2)
        self.gridLayout.addWidget(self.Rewievs, 2, 4, 1, 1)
        self.gridLayout.addWidget(self.Comments, 2, 1, 1, 2)
        self.gridLayout.addWidget(self.Filmtime, 2, 3, 1, 1)
        self.gridLayout.addWidget(self.RatingFrame, 3, 3, 1, 1)
        self.gridLayout.addWidget(self.stackedWidget, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.BestFrame, 4, 1, 1, 4)
        self.gridLayout.addWidget(self.WorstFrame, 5, 1, 1, 4)

        self.setupUi()

    def setupUi(self):
        self.label_top.setText('Experimental')
        self.label_bottom.setText('Experimental')
        self.side_button.setText('Experimental')
        self.CountriesBar.setText('CountriesBar')
        self.GenersBar.setText('GenersBar')
        self.Comments.setText('Comments')
        self.Rewievs.setText('Rewievs')
        self.PieChart.setText('PieChart')
        self.TotalFilms.setText('TotalFilms')
        self.Gistogramma.setText('Gistogramma')
        self.RatingChart.setText('RatingChart')
        self.AvgRating.setText('AvgRating')
        self.BestLabel.setText('Experimental')
        self.worstLabel.setText('Experimental')

        self.Filmtime.setText('filmTime')


if __name__ == "__main__":
    import sys
    import clean_data

    print(clean_data.by_year)
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())

