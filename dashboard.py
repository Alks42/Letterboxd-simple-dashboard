from PyQt5 import QtCore, QtGui, QtWidgets, QtChart


class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.resize(1400, 1000)
        self.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)

        self.gridLayoutWidget = QtWidgets.QWidget()
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1400, 1000))
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 20, 30, 0)

        self.setCentralWidget(self.gridLayoutWidget)
        self.statusbar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusbar)
        self.main_frame = QtWidgets.QFrame(self.gridLayoutWidget)
        self.gridLayout_mf = QtWidgets.QGridLayout(self.main_frame)
        self.gridLayout_mf.setSpacing(0)

        self.frame_to_call_frame = QtWidgets.QFrame(self.gridLayoutWidget)
        self.frame_to_call_frame.setMinimumWidth(30)

        # Side Frame
        self.side_frame = QtWidgets.QFrame(self.gridLayoutWidget)
        self.side_layout = QtWidgets.QVBoxLayout(self.side_frame)
        self.side_button = QtWidgets.QPushButton(self.side_frame)
        self.side_button.setText('Overall')
        self.side_button.clicked.connect(lambda x: self.draw_dashboard(overall, False))

        self.side_layout.addWidget(self.side_button, 0, QtCore.Qt.AlignTop)

        for i in reversed(by_year.keys()):
            self.year_button = QtWidgets.QPushButton(self.side_frame)
            self.year_button.clicked.connect(lambda x, i=i: self.draw_dashboard(by_year[i], year=i))
            self.year_button.setText(str(i))
            self.side_layout.addWidget(self.year_button, 0, QtCore.Qt.AlignTop)

        self.problem_label = QtWidgets.QLabel(self.side_frame)
        self.form = QtWidgets.QLineEdit(self.side_frame)
        self.form.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.checkSave = QtWidgets.QCheckBox(self.side_frame)
        self.checkSave.setText('Save key')
        self.apply_button = QtWidgets.QPushButton(self.side_frame)
        self.apply_button.setText('Apply key')
        self.apply_button.clicked.connect(lambda x: self.restart_with_key(self.form.text()))
        self.checkSave.clicked.connect(lambda x: self.save_key(self.checkSave.checkState()))

        self.checkLock = QtWidgets.QCheckBox(self.side_frame)
        self.checkLock.setText('Lock Side Menu')
        self.label_bottom = QtWidgets.QLabel(self.side_frame)
        self.label_bottom.setText('You\n Are\n Useless')

        self.side_layout.addWidget(self.problem_label, 0, QtCore.Qt.AlignBottom)
        self.side_layout.addWidget(self.form, 0, QtCore.Qt.AlignBottom)
        self.side_layout.addWidget(self.apply_button, 0, QtCore.Qt.AlignBottom)
        self.side_layout.addWidget(self.checkSave, 0, QtCore.Qt.AlignBottom)
        self.side_layout.addWidget(self.checkLock, 0, QtCore.Qt.AlignBottom)
        self.side_layout.addWidget(self.label_bottom, 0, QtCore.Qt.AlignBottom)

        self.gridLayout.addWidget(self.frame_to_call_frame, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.side_frame, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.main_frame, 0, 2, 1, 1)

        self.animation_duration = 512

        self.side_frame.hide()
        self.side_frame.installEventFilter(self)
        self.frame_to_call_frame.installEventFilter(self)
        self.draw_dashboard(overall, False)
        self.restart_with_key(api_key)

    def draw_dashboard(self, data, isyear=True, year=None):

        def explode_slice(slc):
            nonlocal year_cashe
            value = '{:.0f}'.format(slc.value())
            if not slc.isExploded():
                year = str(slc.label())
                year_cashe = year
                slc.setLabelPosition(QtChart.QPieSlice.LabelOutside)
                slc.setLabel(value + ' wached in ' + year)
            else:
                slc.setLabelPosition(QtChart.QPieSlice.LabelInsideHorizontal)
                slc.setLabel(year_cashe)

            slc.setExploded(not slc.isExploded())

        def create_table(data_table):
            nonlocal data
            table = QtWidgets.QTableWidget(self.main_frame)
            table.setColumnCount(5)
            rows = 3 if data[-1] else 2
            table.setRowCount(rows)
            table.horizontalHeader().hide()
            table.verticalHeader().hide()
            table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

            for column in range(5):
                for row in range(rows):
                    item = list(data_table[column].values())[row]
                    table.setItem(row, column, QtWidgets.QTableWidgetItem(str(item)))
            table.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
            table.resizeColumnsToContents()
            return table

        # clear layout
        for i in reversed(range(self.gridLayout_mf.count())):
            self.gridLayout_mf.takeAt(i).widget().setParent(None)
        year_cashe = 0

        # filmtime
        if data[-1]:
            self.Filmtime = QtWidgets.QLabel(self.main_frame)
            self.Filmtime.setText('You spent\n' + "{:.0f}".format(data[-1][2]//60) + ' hours\n' + 'watching films')

        # geners, country
        self.GenersBar = QtWidgets.QLabel(self.main_frame)
        self.CountriesBar = QtWidgets.QLabel(self.main_frame)
        if data[-1]:
            self.GenersBar = self.create_bar(data[-1][0], True)
            self.CountriesBar = self.create_bar(data[-1][1], True)

        # Rating frame
        self.RatingFrame = QtWidgets.QFrame(self.main_frame)
        self.ratinglayout = QtWidgets.QHBoxLayout(self.RatingFrame)
        self.AvgRating = QtWidgets.QLabel(self.RatingFrame)
        self.AvgRating.setText(data[2] + '\nAvg')

        # Reviews, comments
        self.Rewievs = QtWidgets.QLabel(self.RatingFrame)
        self.Comments = QtWidgets.QLabel(self.RatingFrame)
        if not isyear:
            self.Comments.setText('You wrote comments\n' + str(sum(comments.values())))
            self.Rewievs.setText('You wrote reviews\n' + str(sum(reviews.values())))
        else:
            if year not in comments: comments[year] = 0
            if year not in reviews: reviews[year] = 0
            self.Comments.setText('You wrote comments\n' + str(comments[year]))
            self.Rewievs.setText('You wrote reviews\n' + str(reviews[year]))

        self.ratinglayout.addWidget(self.Comments)
        self.ratinglayout.addWidget(self.create_bar(overall[1]))
        self.ratinglayout.addWidget(self.AvgRating)
        self.ratinglayout.addWidget(self.Rewievs)

        # middle chart
        self.PieChart = QtChart.QChart()
        self.series = QtChart.QPieSeries()
        self.series.setHoleSize(0.35)
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
        for key, value in data[5].items():
            slc = QtChart.QPieSlice(str(key), value) if not isyear else QtChart.QPieSlice(months[key-1], value)
            if value > 0: slc.setLabelVisible(True)
            slc.setExplodeDistanceFactor(0.05)
            slc.setLabelPosition(QtChart.QPieSlice.LabelInsideHorizontal)
            # slc.setLabelColor(QtCore.Qt.white)
            slc.hovered.connect(lambda x, slc=slc: explode_slice(slc))
            self.series.append(slc)


        self.PieChart.addSeries(self.series)
        self.chart_view = QtChart.QChartView(self.PieChart)
        self.PieChart.setAnimationOptions(QtChart.QChart.SeriesAnimations)
        self.PieChart.setTitle('You wavhed '+str(data[0])+' films')
        self.PieChart.legend().setVisible(False)
        self.PieChart.setAnimationDuration(self.animation_duration)

        # # Connection using an extra parameter for the slot
        # slc.hovered[bool].connect(partial(self.explode_slice, slc=slc))

        if data[3]:
            # Best table
            self.BestLabel = QtWidgets.QLabel(self.main_frame)
            self.BestLabel.setText('----------------------Best--------------------')
            self.BestTable = create_table(data[3])

            # Worst table
            self.WorstLabel = QtWidgets.QLabel(self.main_frame)
            self.WorstLabel.setText('---------------------Worst---------------------')
            self.WorstTable = create_table(data[4])


        self.gridLayout_mf.addWidget(self.chart_view, 0, 1, 1, 1)
        if data[-1]:
            self.gridLayout_mf.addWidget(self.CountriesBar, 0, 2, 2, 1)
            self.gridLayout_mf.addWidget(self.GenersBar, 0, 0, 2, 1)
            self.gridLayout_mf.addWidget(self.Filmtime, 1, 1, 1, 1)
        self.gridLayout_mf.addWidget(self.RatingFrame, 2, 0, 1, 3)
        if data[3]:
            self.gridLayout_mf.addWidget(self.BestLabel, 3, 0, 1, 3)
            self.gridLayout_mf.addWidget(self.BestTable, 4, 0, 1, 3)
            self.gridLayout_mf.addWidget(self.WorstLabel, 5, 0, 1, 3)
            self.gridLayout_mf.addWidget(self.WorstTable, 6, 0, 1, 3)

    def create_bar(self, df, isvertical=False):
        self.barchart = QtChart.QChart()
        self.barset = QtChart.QBarSet('rate')
        self.axis = QtChart.QBarCategoryAxis()

        if not isvertical:
            self.barchart.setTitle('Rating')
            self.bar_series = QtChart.QBarSeries()
            bar_data = df
            self.barchart.setAxisX(self.axis)
        else:
            self.bar_series = QtChart.QHorizontalBarSeries()
            bar_data = dict(sorted(df.items(), key=lambda item: item[1])[:10])
            self.barchart.setAxisY(self.axis)

        self.axis.append(str(k) for k in bar_data.keys())
        for value in bar_data.values():
            self.barset.append(value)
        self.bar_series.append(self.barset)
        self.barchart.addSeries(self.bar_series)
        self.chart_view = QtChart.QChartView(self.barchart)

        self.barchart.setAnimationOptions(QtChart.QChart.SeriesAnimations)
        self.barchart.setAnimationDuration(self.animation_duration)
        self.barchart.legend().setVisible(False)
        return self.chart_view

    def save_key(self, state):
        if state == 2 and len(self.form.text()) > 30:
            with open('YourAPIKey.txt', 'w') as f:
                f.write(self.form.text().strip())

    def restart_with_key(self, api_key_new):
        global api_key
        if api_key_new:
            api_key = api_key_new
            self.api_process_start()
            self.save_key(self.checkSave.checkState())
            self.form.setText('')
        else:
            self.problem_label.setText('No valid api key found')

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

    def api_process_start(self):
        self.process = Api_process()
        self.process.start()
        self.process.update.connect(self.api_process_update)

    def api_process_update(self, args):
        global overall, by_year, problems, comments, reviews
        if type(args) == str: self.problem_label.setText(args)
        else:
            overall, by_year, problems, comments, reviews = args
            if problems == 0: self.problem_label.setText('Ran into no films with problems.')
            else:
                self.problem_label.setText('Ran into ' + str(problems) + '\nfilms with problems.')

            self.draw_dashboard(overall, False)


class Api_process(QtCore.QThread):
    update = QtCore.pyqtSignal(object)

    def run(self):
        global api_key
        if api_key:
            self.update.emit("Handaling data...")
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

    overall, by_year, problems, comments, reviews = clean_data.main()
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())

