from PyQt6 import QtCore, QtGui, QtWidgets, QtCharts


class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.resize(1080, 800)
        # self.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)

        self.gridLayoutWidget = QtWidgets.QWidget()
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1080, 1700))
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        # self.setAutoFillBackground(True)
        # self.setStyleSheet('background-color: black')

        self.setCentralWidget(self.gridLayoutWidget)
        self.statusbar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusbar)

        self.frame_to_call_frame = QtWidgets.QFrame(self.gridLayoutWidget)
        self.frame_to_call_frame.setMinimumWidth(30)
        self.frame_to_call_frame.setStyleSheet("QFrame {border-radius:3;"
                                               "background-color: rgb(200, 255, 255);"
                       "border-right: 4 inset #000000;}"
                       )

        # Side Frame
        self.side_frame = QtWidgets.QFrame(self.gridLayoutWidget)
        self.side_layout = QtWidgets.QVBoxLayout(self.side_frame)


        for i in reversed(range(len(films_by_year.keys()))):
            year_button = QtWidgets.QPushButton(self.side_frame)
            year_button.clicked.connect(lambda x, i=i: self.stacked.setCurrentIndex(i))
            year_button.setText(str(list(films_by_year.keys())[i]))
            self.side_layout.addWidget(year_button, 0, QtCore.Qt.AlignmentFlag.AlignTop)

        self.problem_label = QtWidgets.QLabel(self.side_frame)
        self.form = QtWidgets.QLineEdit(self.side_frame)
        self.form.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Minimum)
        self.checkSave = QtWidgets.QCheckBox(self.side_frame)
        self.checkSave.setText('Save key')
        self.apply_button = QtWidgets.QPushButton(self.side_frame)
        self.apply_button.setText('Apply key')
        self.apply_button.clicked.connect(lambda x: self.restart_with_key(self.form.text()))
        self.checkSave.clicked.connect(lambda x: self.save_key(self.checkSave.checkState().value))

        self.checkLock = QtWidgets.QCheckBox(self.side_frame)
        self.checkLock.setText('Lock Side Menu')
        self.label_bottom = QtWidgets.QLabel(self.side_frame)
        self.label_bottom.setText('You\n Are\n Useless')

        self.side_layout.addWidget(self.problem_label, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.side_layout.addWidget(self.form, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.side_layout.addWidget(self.apply_button, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.side_layout.addWidget(self.checkSave, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.side_layout.addWidget(self.checkLock, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.side_layout.addWidget(self.label_bottom, 0, QtCore.Qt.AlignmentFlag.AlignBottom)

        self.side_frame.setStyleSheet("QFrame {background-color: rgb(200, 255, 255);"
                       "border-right: 4 solid #000000;}"
                       )

        #--------------------------------------------------------------------------------

        self.gridLayout.addWidget(self.frame_to_call_frame, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.side_frame, 0, 1, 1, 1)

        self.animation_duration = 512

        self.side_frame.hide()
        self.side_frame.installEventFilter(self)
        self.frame_to_call_frame.installEventFilter(self)
        self.stacked = False
        self.draw_stacked()
        self.restart_with_key(api_key)

    def draw_stacked(self):
        global films_by_year

        def explode_slice(slc, all):
            nonlocal year_cashe
            percent = '{:.0f}'.format(slc.value() / all * 100)
            value = '{:.0f}'.format(slc.value())
            if not slc.isExploded():
                year = str(slc.label())
                year_cashe = year
                slc.setLabelPosition(QtCharts.QPieSlice.LabelPosition.LabelOutside)
                slc.setLabel(value + ' ({}%)'.format(percent))
            else:
                slc.setLabelPosition(QtCharts.QPieSlice.LabelPosition.LabelInsideHorizontal)
                slc.setLabel(year_cashe)

            slc.setExploded(not slc.isExploded())

        def create_table(data_table):
            table = QtWidgets.QTableWidget(main_frame)
            table.setColumnCount(5)
            table.setRowCount(2)
            table.horizontalHeader().hide()
            table.verticalHeader().hide()
            table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

            for row in range(2):
                key = list(data_table.keys())[row]
                for column in range(5):
                    item = data_table[key][column]
                    table.setItem(row, column, QtWidgets.QTableWidgetItem(str(item)))
            table.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
            table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
            table.resizeColumnsToContents()
            return table

        if self.stacked:
            self.stacked.setParent(None)
        year_cashe = 0

        self.stacked = QtWidgets.QStackedWidget(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.stacked, 0, 2, 1, 1)


        for year in films_by_year.keys():
            data = films_by_year[year]
            main_frame = QtWidgets.QFrame()
            main_frame.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                          QtWidgets.QSizePolicy.Policy.Expanding)
            gridLayout_mf = QtWidgets.QGridLayout(main_frame)
            gridLayout_mf.setSpacing(0)

            # middle chart
            PieChart = QtCharts.QChart()
            PieChart.setTitle('You wached '+str(data[0])+' films')
            PieChart.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)
            PieChart.legend().setVisible(False)
            PieChart.setAnimationDuration(self.animation_duration)
            PieChart.setContentsMargins(-30, -30, -30, -30)

            series = QtCharts.QPieSeries()
            series.setHoleSize(0.35)

            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
            for key, value in data[5].items():
                slc = QtCharts.QPieSlice(str(key), value) if year =='Overall' else QtCharts.QPieSlice(months[key-1], value)
                if value > 0: slc.setLabelVisible(True)
                slc.setExplodeDistanceFactor(0.05)
                slc.setLabelPosition(QtCharts.QPieSlice.LabelPosition.LabelInsideHorizontal)
                slc.hovered.connect(lambda x, slc=slc, data=data: explode_slice(slc, data[0]))
                series.append(slc)

            PieChart.addSeries(series)
            chart_view = QtCharts.QChartView(PieChart)
            chart_view.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                     QtWidgets.QSizePolicy.Policy.Expanding)
            gridLayout_mf.addWidget(chart_view, 0, 1, 1, 1)

            # Rating frame, reviews, comments
            RatingFrame = QtWidgets.QFrame(main_frame)
            ratinglayout = QtWidgets.QHBoxLayout(RatingFrame)
            AvgRating = QtWidgets.QLabel(RatingFrame)

            Rewievs = QtWidgets.QLabel(RatingFrame)
            Comments = QtWidgets.QLabel(RatingFrame)

            ratinglayout.addWidget(Comments)
            ratinglayout.addWidget(self.create_bar(data[1]), QtCore.Qt.AlignmentFlag.AlignCenter)
            ratinglayout.addWidget(AvgRating)
            ratinglayout.addWidget(Rewievs)

            if year=='Overall':
                Comments.setText('You wrote comments\n' + str(sum(comments.values())))
                Rewievs.setText('You wrote reviews\n' + str(sum(reviews.values())))
            else:
                if year not in comments: comments[year] = 0
                if year not in reviews: reviews[year] = 0
                Comments.setText('You wrote comments\n' + str(comments[year]))
                Rewievs.setText('You wrote reviews\n' + str(reviews[year]))
            AvgRating.setText(data[2] + '\nAvg')

            RatingFrame.setMaximumHeight(200)
            gridLayout_mf.addWidget(RatingFrame, 2, 0, 1, 3)
            if data[3]:
                # Best table
                BestLabel = QtWidgets.QLabel(main_frame)
                BestLabel.setText('----------------------Best--------------------')
                BestTable = create_table(data[3])

                # Worst table
                WorstLabel = QtWidgets.QLabel(main_frame)
                WorstLabel.setText('---------------------Worst---------------------')
                WorstTable = create_table(data[4])

                gridLayout_mf.addWidget(BestLabel, 3, 0, 1, 3, QtCore.Qt.AlignmentFlag.AlignCenter)
                gridLayout_mf.addWidget(BestTable, 4, 0, 1, 3, QtCore.Qt.AlignmentFlag.AlignCenter)
                gridLayout_mf.addWidget(WorstLabel, 5, 0, 1, 3, QtCore.Qt.AlignmentFlag.AlignCenter)
                gridLayout_mf.addWidget(WorstTable, 6, 0, 1, 3, QtCore.Qt.AlignmentFlag.AlignCenter)

            if data[-1]:
                GenersBar = self.create_bar(data[-1][0], True)
                CountriesBar = self.create_bar(data[-1][1], True)

                GenersBar.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                              QtWidgets.QSizePolicy.Policy.Expanding)
                CountriesBar.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                              QtWidgets.QSizePolicy.Policy.Expanding)

                gridLayout_mf.addWidget(CountriesBar, 0, 2, 2, 1)
                gridLayout_mf.addWidget(GenersBar, 0, 0, 2, 1)

                Filmtime = QtWidgets.QLabel(main_frame)
                Filmtime.setText('You spent\n' + "{:.0f}".format(data[-1][2]//60) + ' hours\n' + 'watching films')
                gridLayout_mf.addWidget(Filmtime, 1, 1, 1, 1)

            self.stacked.addWidget(main_frame)
        self.stacked.setCurrentIndex(len(films_by_year.keys())-1)

    def hovered(self, series):
        if series.isLabelsVisible(): series.setLabelsVisible(False)
        else: series.setLabelsVisible(True)

    def create_bar(self, df, isvertical=False):

        barchart = QtCharts.QChart()
        axis = QtCharts.QBarCategoryAxis()

        if not isvertical:
            barchart.setTitle('Rating')
            bar_series = QtCharts.QBarSeries()
            bar_data = df
            barchart.addAxis(axis, QtCore.Qt.AlignmentFlag.AlignBottom)
            bar_series.setLabelsPosition(QtCharts.QBarSeries.LabelsPosition.LabelsOutsideEnd)
        else:
            bar_series = QtCharts.QHorizontalBarSeries()
            bar_data = dict(sorted(df.items(), key=lambda item: item[1])[-10:])
            bar_series.setLabelsPosition(QtCharts.QBarSeries.LabelsPosition.LabelsInsideEnd)
            barchart.addAxis(axis, QtCore.Qt.AlignmentFlag.AlignLeft)

        axis.append(str(k) for k in bar_data.keys())
        axis.setGridLineVisible(False)
        barset = QtCharts.QBarSet('default')
        barset.append(list(bar_data.values()))
        bar_series.append(barset)
        barchart.addSeries(bar_series)
        chart_view = QtCharts.QChartView(barchart)

        barchart.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)
        barchart.setAnimationDuration(self.animation_duration)
        barchart.legend().setVisible(False)
        bar_series.hovered.connect(lambda x: self.hovered(bar_series))
        return chart_view

    def save_key(self, state):
        if state == 2 and len(self.form.text()) > 30:
            with open('YourAPIKey.txt', 'w') as f:
                f.write(self.form.text().strip())

    def restart_with_key(self, api_key_new):
        global api_key
        if api_key_new:
            api_key = api_key_new
            self.api_process_start()
            self.save_key(self.checkSave.checkState().value)
            self.form.setText('')

    def eventFilter(self, obj, event):
        if obj is self.frame_to_call_frame and event.type() == QtCore.QEvent.Type.Enter:
            self.frame_to_call_frame.hide()
            self.side_frame.show()
            return True
        elif obj is self.side_frame and event.type() == QtCore.QEvent.Type.Leave and  self.checkLock.checkState().value == 0:
            self.side_frame.hide()
            self.frame_to_call_frame.show()
            return True
        return super().eventFilter(obj, event)

    def api_process_start(self):
        self.process = Api_process()
        self.process.start()
        self.process.update.connect(self.api_process_update)

    def api_process_update(self, args):
        global films_by_year, problems, comments, reviews
        if type(args) == str:
            self.problem_label.setText(args)
        else:
            films_by_year, problems, comments, reviews = args
            if problems == 0: self.problem_label.setText('Ran into no films with problems.')
            else:
                self.problem_label.setText('Ran into ' + str(problems) + '\nfilms with problems.')

            self.draw_stacked()


class Api_process(QtCore.QThread):
    update = QtCore.pyqtSignal(object)

    def run(self):
        global api_key
        if api_key:
            self.update.emit("Handaling data. \nIt might take a while.")
            sc = requests.get('https://api.themoviedb.org/3/search/movie?api_key=' + api_key + '&query=Memento')
            if sc.status_code != 200:
                self.update.emit("No valid key found!")
                api_key = ''
            else:
                self.update.emit(clean_data.main(api_key))


if __name__ == "__main__":
    import sys
    import clean_data
    import requests

    api_key = ''
    with open('YourAPIKey.txt') as f:
        api_key = f.read()

    films_by_year, problems, comments, reviews = clean_data.main()
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec())

