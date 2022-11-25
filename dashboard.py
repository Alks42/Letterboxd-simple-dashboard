from PyQt6 import QtCore, QtGui, QtWidgets, QtCharts


class Page_with_data(QtWidgets.QFrame):
    def __init__(self, data, year):
        super(Page_with_data, self).__init__()
        self.data, self.year = data, year
        self.bar_color = '#ed8e00'

        self.gridLayout_mf = QtWidgets.QGridLayout()
        self.setLayout(self.gridLayout_mf)
        self.gridLayout_mf.setContentsMargins(10, 10, 20, 0)
        self.gridLayout_mf.setSpacing(0)
        # middle chart
        self.pie_chart = QtCharts.QChart()
        self.series = QtCharts.QPieSeries()
        self.pie_chart.addSeries(self.series)
        self.setup_pie_chart()
        self.chart_view = QtCharts.QChartView(self.pie_chart)
        self.chart_view.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.chart_view.setRenderHint(
            QtGui.QPainter.RenderHint.Antialiasing | QtGui.QPainter.RenderHint.TextAntialiasing)
        self.gridLayout_mf.addWidget(self.chart_view, 0, 1, 1, 1)
        self.rating_frame = QtWidgets.QFrame()
        self.avg_rate = QtWidgets.QLabel(self.rating_frame)
        self.rating_layout = QtWidgets.QHBoxLayout(self.rating_frame)
        self.rating_chart = self.create_bar(self.data[1])
        # reviews, comments
        self.reviews_label = QtWidgets.QLabel(self.rating_frame)
        self.comments_label = QtWidgets.QLabel(self.rating_frame)
        self.setup_rating_and_comments()

        self.rating_layout.setSpacing(30)
        self.rating_layout.addWidget(self.comments_label)
        self.rating_layout.addWidget(self.rating_chart)
        self.rating_layout.addWidget(self.avg_rate)
        self.rating_layout.addWidget(self.reviews_label)

        self.gridLayout_mf.addWidget(self.rating_frame, 2, 0, 1, 3, QtCore.Qt.AlignmentFlag.AlignCenter)
        # api data if exists
        if self.data[-1]:
            self.geners_bar = self.create_bar(self.data[-1][0], True)
            self.countries_bar = self.create_bar(self.data[-1][1], True)
            self.geners_bar.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
            self.countries_bar.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
            self.film_time = QtWidgets.QLabel()
            self.film_time.setText('<center>You spent time:<br>' + "{:.0f}".format(self.data[-1][2] / 60) + ' hours')

            self.gridLayout_mf.addWidget(self.countries_bar, 0, 2, 1, 1)
            self.gridLayout_mf.addWidget(self.geners_bar, 0, 0, 1, 1)
            self.gridLayout_mf.addWidget(self.film_time, 1, 1, 1, 1)
        # Tables if exists
        if self.data[3]:
            # Best table
            self.best_label = QtWidgets.QLabel()
            self.best_label.setText('Top 5 highest rated films')
            self.best_label.setObjectName('table_label')
            self.best_table = self.create_table(self.data[3])
            # Worst table
            self.worst_label = QtWidgets.QLabel()
            self.worst_label.setText('Top 5 lowest rated films')
            self.worst_label.setObjectName('table_label')
            self.worst_table = self.create_table(self.data[4])

            self.gridLayout_mf.addWidget(self.best_label, 3, 0, 1, 3, QtCore.Qt.AlignmentFlag.AlignCenter)
            self.gridLayout_mf.addWidget(self.best_table, 4, 0, 1, 3, QtCore.Qt.AlignmentFlag.AlignCenter)
            self.gridLayout_mf.addWidget(self.worst_label, 5, 0, 1, 3, QtCore.Qt.AlignmentFlag.AlignCenter)
            self.gridLayout_mf.addWidget(self.worst_table, 6, 0, 1, 3, QtCore.Qt.AlignmentFlag.AlignCenter)

    def setup_pie_chart(self):

        def explode_slice(slc, all):
            nonlocal year_cashe
            percent, value = '{:.0f}'.format(slc.value() / all * 100), '{:.0f}'.format(slc.value())
            if not slc.isExploded():
                year_cashe = str(slc.label())
                slc.setLabelColor(QtGui.QColor('white'))
                slc.setLabelPosition(QtCharts.QPieSlice.LabelPosition.LabelOutside)
                slc.setLabel(value + ' ({}%)'.format(percent))
            else:
                slc.setLabelColor(QtGui.QColor('black'))
                slc.setLabelPosition(QtCharts.QPieSlice.LabelPosition.LabelInsideNormal)
                slc.setLabel(year_cashe)
            slc.setExploded(not slc.isExploded())

        year_cashe = 0
        self.pie_chart.setTitle('<center>You wached <br> ' + str(self.data[0]) + ' films</center>')
        self.pie_chart.setTitleFont(QtGui.QFont('Century Gothic', 14))
        self.pie_chart.setTitleBrush(QtGui.QColor('white'))
        self.pie_chart.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)
        self.pie_chart.legend().setVisible(False)
        self.pie_chart.setAnimationDuration(512)
        self.pie_chart.setMargins(QtCore.QMargins(-5, 0, -5, -42))
        self.pie_chart.setBackgroundBrush(QtGui.QBrush(QtGui.QColor("transparent")))

        self.series.setHoleSize(0.25)
        self.series.setPieSize(0.6)

        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
        green = 175
        for key, value in self.data[5].items():
            if self.year == 'Overall':
                slc = QtCharts.QPieSlice(str(key), value)
            else:
                slc = QtCharts.QPieSlice(months[key - 1], value)
            if value > 0: slc.setLabelVisible(True)
            slc.setExplodeDistanceFactor(0.05)
            slc.setBorderWidth(0)
            slc.setLabelFont((QtGui.QFont('Segoe MDL2 Assets', 10)))
            slc.setColor(QtGui.QColor(0, green, 255))
            green += 15
            if green > 255: green = 200
            slc.setLabelPosition(QtCharts.QPieSlice.LabelPosition.LabelInsideNormal)
            slc.hovered.connect(lambda x, slc=slc, data=self.data: explode_slice(slc, self.data[0]))
            self.series.append(slc)

    def setup_rating_and_comments(self):
        self.rating_chart.setMinimumSize(315, 150)
        self.avg_rate.setText(self.data[2] + '\nAvg')
        self.avg_rate.setObjectName('avg')
        if self.year == 'Overall':
            self.comments_label.setText(f'<center>You wrote:<br>{sum(comments.values())} comments')
            self.reviews_label.setText(f'<center>You wrote:<br>{sum(reviews.values())} reviews')
        else:
            self.comments_label.setText(
                f'<center>You wrote:<br>{comments[self.year] if self.year in comments else 0} comments')
            self.reviews_label.setText(
                f'<center>You wrote:<br>{reviews[self.year] if self.year in reviews else 0} reviews')

    def create_bar(self, df, is_vertical=False):
        self.bar_color = '#ed8e00' if self.bar_color != '#ed8e00' else '#06ad00'

        barchart = QtCharts.QChart()
        barset = QtCharts.QBarSet('default')
        axis = QtCharts.QBarCategoryAxis()
        barset.setBorderColor(QtGui.QColor(0, 0, 1))
        if not is_vertical:
            bar_series = QtCharts.QBarSeries()
            bar_data = df
            bar_series.setBarWidth(1)
            barchart.addAxis(axis, QtCore.Qt.AlignmentFlag.AlignBottom)
            bar_series.setLabelsPosition(QtCharts.QBarSeries.LabelsPosition.LabelsOutsideEnd)
            barset.setColor(QtGui.QColor('#575957'))
            # make plot area slightly bigger to fit lables
            axisY = QtCharts.QValueAxis()
            axisY.setVisible(False)
            axisY.setRange(0, max(bar_data.values()) * 1.4)
            barchart.addAxis(axisY, QtCore.Qt.AlignmentFlag.AlignLeft)

        else:
            bar_series = QtCharts.QHorizontalBarSeries()
            [df.update({'\0' * i: 0}) for i in range(10 - len(df)) if len(df) < 10]
            bar_data = dict(sorted(df.items(), key=lambda item: item[1])[-10:])
            bar_series.setLabelsPosition(QtCharts.QBarSeries.LabelsPosition.LabelsCenter)
            barchart.addAxis(axis, QtCore.Qt.AlignmentFlag.AlignLeft)
            barset.setColor(QtGui.QColor(self.bar_color))

        axis.setLineVisible(False)
        axis.append(str(k) for k in bar_data)
        axis.setLabelsColor(QtGui.QColor('white'))
        axis.setGridLineVisible(False)
        axis.setTruncateLabels(False)
        barset.append(list(bar_data.values()))
        barset.setLabelFont((QtGui.QFont('Segoe MDL2 Assets', 12)))
        bar_series.append(barset)
        barchart.addSeries(bar_series)
        if not is_vertical: bar_series.attachAxis(axisY)
        bar_series.hovered.connect(lambda x: bar_series.setLabelsVisible(not bar_series.isLabelsVisible()))
        barchart.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)
        barchart.setAnimationDuration(512)
        barchart.legend().setVisible(False)
        barchart.setMargins(QtCore.QMargins(-5, -5, -5, -5))
        barchart.setBackgroundRoundness(0)
        barchart.setBackgroundBrush(QtGui.QBrush(QtGui.QColor("transparent")))

        chart_view = QtCharts.QChartView(barchart)
        chart_view.setBackgroundBrush(QtGui.QBrush(QtGui.QColor("transparent")))
        chart_view.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing | QtGui.QPainter.RenderHint.TextAntialiasing)
        return chart_view

    def create_table(self, data_table):
        table = QtWidgets.QTableWidget()
        table.setColumnCount(5)
        table.setRowCount(2)
        table.horizontalHeader().hide()
        table.verticalHeader().hide()

        for row in range(2):
            key = list(data_table.keys())[row]
            for column in range(5):
                item = data_table[key][column]
                table.setItem(row, column, QtWidgets.QTableWidgetItem('      ' + str(item)))
                table.item(row, column).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QTableWidget.horizontalHeader(table).ResizeMode.ResizeToContents)
        table.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)
        table.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        table.setSelectionMode(QtWidgets.QTableWidget.SelectionMode.NoSelection)
        return table


class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.resize(1080, 800)

        self.gridLayoutWidget = QtWidgets.QWidget()
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1080, 800))
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle('Letterboxd Simple Dashboard')
        self.setWindowIcon(QtGui.QIcon('lsa.ico'))
        self.setAutoFillBackground(False)
        self.setCentralWidget(self.gridLayoutWidget)
        ###################################################################################
        # Side Frame
        self.side_frame = QtWidgets.QFrame(self.gridLayoutWidget)
        self.side_layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.TopToBottom, self.side_frame)
        self.side_frame.setObjectName('menu')
        self.side_animation = QtCore.QPropertyAnimation(self.side_frame, b"maximumWidth", self)
        self.side_animation.setDuration(200)

        for i in reversed(range(len(films_by_year))):
            year_button = QtWidgets.QPushButton(self.side_frame)
            year_button.clicked.connect(lambda x, i=i: self.stacked.setCurrentIndex(i))
            year_button.setText(str(list(films_by_year.keys())[i]))
            year_button.setContentsMargins(5, 5, 5, 5)
            self.side_layout.addWidget(year_button, 0, QtCore.Qt.AlignmentFlag.AlignTop)

        self.stretch = QtWidgets.QLabel(self.side_frame)
        self.side_layout.addWidget(self.stretch)
        self.side_layout.setStretchFactor(self.stretch, 1)
        self.problem_label = QtWidgets.QLabel(self.side_frame)
        self.problem_label.setContentsMargins(10, 10, 0, 10)
        self.side_width = self.problem_label.width() + 100
        ###################################################################################
        # api key
        self.form = QtWidgets.QLineEdit(self.side_frame)
        self.form.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Minimum)
        self.checkSave = QtWidgets.QCheckBox(self.side_frame)
        self.checkSave.setText('Save key')
        self.checkSave.clicked.connect(lambda x: self.save_key(self.checkSave.checkState().value))

        self.apply_button = QtWidgets.QPushButton(self.side_frame)
        self.apply_button.setText('Apply key')
        self.apply_button.setObjectName('apply_btn')
        self.apply_button.clicked.connect(lambda x: self.process_start(self.form.text()))

        self.checkLock = QtWidgets.QCheckBox(self.side_frame)
        self.checkLock.setText('Lock Side Menu')
        ###################################################################################
        # label with queistions
        self.label_bottom = QtWidgets.QPushButton(self.side_frame)
        self.label_bottom.setObjectName('bottom')
        self.label_bottom.setText('How do i get my data?\nWhere can I get api key?')
        self.label_bottom.clicked.connect(
            lambda x: webbrowser.open('https://github.com/Alks42/Letterboxd-simple-dashboard'))
        self.label_bottom.setContentsMargins(5, 5, 5, 5)
        ###################################################################################
        self.side_layout.setContentsMargins(30, 30, 20, 20)
        self.side_layout.setSpacing(15)
        self.side_layout.addWidget(self.problem_label, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.side_layout.addWidget(self.form, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.side_layout.addWidget(self.apply_button, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.side_layout.addWidget(self.checkSave, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.side_layout.addWidget(self.checkLock, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.side_layout.addWidget(self.label_bottom, 0, QtCore.Qt.AlignmentFlag.AlignBottom)

        self.gridLayout.addWidget(self.side_frame, 0, 0, 3, 1)
        ###################################################################################
        # tmdb label
        self.tmdb = QtWidgets.QPushButton()
        self.tmdb.setObjectName('tmdb')
        self.tmdb.setText('Film data was provided by TMDB')
        self.tmdb.clicked.connect(lambda x: webbrowser.open('https://www.themoviedb.org/'))
        ###################################################################################
        self.side_frame.installEventFilter(self)
        # comment first line and uncomment second to keep side menu on start
        # self.side_frame.setMaximumWidth(10)
        self.checkLock.setChecked(True)

        self.stacked = False
        self.draw_stacked()
        self.process_start(api_key)

    def draw_stacked(self):
        # clear widget
        if self.stacked: self.stacked.setParent(None)
        self.stacked = QtWidgets.QStackedWidget(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.stacked, 0, 1, 1, 1)

        # draw for every year
        for year in films_by_year:
            page = Page_with_data(films_by_year[year], year)
            self.stacked.addWidget(page)
        self.stacked.setCurrentIndex(len(films_by_year) - 1)

    def save_key(self, state):
        if state == 2 and len(self.form.text()) >= 32:
            try:
                sc = requests.get('https://api.themoviedb.org/3/search/movie?api_key=' + api_key + '&query=Memento')
                if sc.status_code == 200:
                    with open('YourAPIKey.txt', 'w') as f:
                        f.write(self.form.text().strip())
            except requests.exceptions.ConnectionError:
                self.problem_label.setObjectName('notKey')
                self.problem_label.setText("Connection error")

    def process_start(self, api_key_new=""):
        global api_key
        if api_key_new:
            api_key = api_key_new
            self.save_key(self.checkSave.checkState().value)
            self.form.setText('')
        self.process = Api_process()
        self.process.start()
        self.process.update.connect(self.process_update)

    def process_update(self, args):
        global films_by_year, problems, comments, reviews
        if type(args) == str:
            self.problem_label.setText(args)
            self.problem_label.setObjectName('notKey') if len(args) <= 19 else self.problem_label.setObjectName('Key')
        else:
            films_by_year, problems, comments, reviews = args
            if problems == 0:
                self.problem_label.setText('No errors occurred\n with films.')
                self.problem_label.setObjectName('notProblem')
            else:
                self.problem_label.setText('Errors occurred with\n' + str(problems) + ' films.')
                self.problem_label.setObjectName('Problem')
            self.gridLayout.addWidget(self.tmdb, 1, 1, 1, 1)
            self.draw_stacked()

        self.side_frame.hide()
        self.setStyleSheet(style)
        self.side_layout.itemAt(0).widget().setFocus()
        self.side_frame.show()

    def eventFilter(self, obj, event):
        if obj is self.side_frame and event.type() == QtCore.QEvent.Type.Enter and self.checkLock.checkState().value == 0:
            self.side_animation.setStartValue(10)
            self.side_animation.setEndValue(self.side_width)
            self.side_animation.start()
            return True
        elif obj is self.side_frame and event.type() == QtCore.QEvent.Type.Leave and self.checkLock.checkState().value == 0:
            self.side_animation.setStartValue(self.side_frame.width())
            self.side_animation.setEndValue(10)
            self.side_animation.start()
            return True
        return super().eventFilter(obj, event)


class Api_process(QtCore.QThread):
    update = QtCore.pyqtSignal(object)

    def run(self):
        global api_key
        self.update.emit("Handaling data. \nIt might take a while.")
        try:
            # check to make sure api_key is valid
            sc = requests.get('https://api.themoviedb.org/3/search/movie?api_key=' + api_key + '&query=Memento')
            if sc.status_code == 200:
                self.update.emit(clean_data.main(api_key))
            else:
                self.update.emit("No valid key found!")
        except requests.exceptions.ConnectionError:
            self.update.emit("Connection error!")


if __name__ == "__main__":
    import sys
    import clean_data
    import requests
    import webbrowser

    api_key = ''
    with open('YourAPIKey.txt') as f:
        api_key = f.read()
    with open('Style.css') as f:
        style = f.read()

    films_by_year, problems, comments, reviews = clean_data.main()
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec())
