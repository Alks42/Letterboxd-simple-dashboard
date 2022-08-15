from PyQt6 import QtCore, QtGui, QtWidgets, QtCharts

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

        # Side Frame
        self.side_frame = QtWidgets.QFrame(self.gridLayoutWidget)
        self.side_layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.Direction.TopToBottom, self.side_frame)
        self.side_frame.setObjectName('menu')
        self.side_animation = QtCore.QPropertyAnimation(self.side_frame, b"maximumWidth", self)
        self.side_animation.setDuration(200)

        for i in reversed(range(len(films_by_year.keys()))):
            year_button = QtWidgets.QPushButton(self.side_frame)
            year_button.clicked.connect(lambda x, i=i: self.stacked.setCurrentIndex(i))
            year_button.setText(str(list(films_by_year.keys())[i]))
            year_button.setContentsMargins(5,5,5,5)
            self.side_layout.addWidget(year_button, 0, QtCore.Qt.AlignmentFlag.AlignTop)

        self.stretch = QtWidgets.QLabel(self.side_frame)
        self.side_layout.addWidget(self.stretch)
        self.side_layout.setStretchFactor(self.stretch, 1)
        self.problem_label = QtWidgets.QLabel(self.side_frame)
        self.problem_label.setContentsMargins(10,10,0,10)
        self.side_width = self.problem_label.width() + 100

            # api key
        self.form = QtWidgets.QLineEdit(self.side_frame)
        self.form.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Minimum)
        self.checkSave = QtWidgets.QCheckBox(self.side_frame)
        self.checkSave.setText('Save key')
        self.apply_button = QtWidgets.QPushButton(self.side_frame)
        self.apply_button.setText('Apply key')
        self.apply_button.setObjectName('apply_btn')

        self.apply_button.clicked.connect(lambda x: self.restart_with_key(self.form.text()))
        self.checkSave.clicked.connect(lambda x: self.save_key(self.checkSave.checkState().value))

        self.checkLock = QtWidgets.QCheckBox(self.side_frame)
        self.checkLock.setText('Lock Side Menu')

            #label with queistions
        self.label_bottom = QtWidgets.QPushButton(self.side_frame)
        self.label_bottom.setObjectName('bottom')
        self.label_bottom.setText('How do i get my data?\nWhere can I get api key?')
        self.label_bottom.clicked.connect(lambda x: webbrowser.open('https://github.com/Alks42/Letterboxd-simple-dashboard'))
        self.label_bottom.setContentsMargins(5,5,5,5)

        self.side_layout.setContentsMargins(30,30,20,20)
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

        self.animation_duration = 512
        self.bar_color = '#06ad00'

        self.side_frame.installEventFilter(self)
        # coment first and uncoment second to keep side menu on start
        # self.side_frame.setMaximumWidth(10)
        self.checkLock.setChecked(True)

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
                slc.setLabelColor(QtGui.QColor('white'))
                slc.setLabelPosition(QtCharts.QPieSlice.LabelPosition.LabelOutside)
                slc.setLabel(value + ' ({}%)'.format(percent))
            else:
                slc.setLabelColor(QtGui.QColor('black'))
                slc.setLabelPosition(QtCharts.QPieSlice.LabelPosition.LabelInsideNormal)
                slc.setLabel(year_cashe)

            slc.setExploded(not slc.isExploded())

        def create_table(data_table):
            table = QtWidgets.QTableWidget(main_frame)
            table.setColumnCount(5)
            table.setRowCount(2)
            table.horizontalHeader().hide()
            table.verticalHeader().hide()

            for row in range(2):
                key = list(data_table.keys())[row]
                for column in range(5):
                    item = data_table[key][column]
                    table.setItem(row, column, QtWidgets.QTableWidgetItem('      '+str(item)))
                    table.item(row, column).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # it would be much easier to use Qlabels instead
            table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
            table.horizontalHeader().setSectionResizeMode(QtWidgets.QTableWidget.horizontalHeader(table).ResizeMode.ResizeToContents)
            table.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.NoEditTriggers)
            table.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
            table.setSelectionMode(QtWidgets.QTableWidget.SelectionMode.NoSelection)
            return table

        # clear widget
        if self.stacked:
            self.stacked.setParent(None)
        year_cashe = 0

        self.stacked = QtWidgets.QStackedWidget(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.stacked, 0, 1, 1, 1)

        # draw for every year
        for year in films_by_year.keys():
            data = films_by_year[year]
            main_frame = QtWidgets.QFrame()
            main_frame.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                          QtWidgets.QSizePolicy.Policy.Expanding)
            gridLayout_mf = QtWidgets.QGridLayout(main_frame)
            gridLayout_mf.setContentsMargins(10,10,20,0)
            gridLayout_mf.setSpacing(0)

            # middle chart
            pie_chart = QtCharts.QChart()
            pie_chart.setTitle('<center>You wached <br> '+str(data[0])+' films</center>')
            pie_chart.setTitleFont(QtGui.QFont('Century Gothic', 14))
            pie_chart.setTitleBrush(QtGui.QColor('white'))
            pie_chart.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)
            pie_chart.legend().setVisible(False)
            pie_chart.setAnimationDuration(self.animation_duration)
            pie_chart.setMargins(QtCore.QMargins(-5, -5, -5, -5))
            pie_chart.setBackgroundBrush(QtGui.QBrush(QtGui.QColor("transparent")))

            series = QtCharts.QPieSeries()
            series.setHoleSize(0.25)
            series.setPieSize(0.6)

            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
            green = 175
            for key, value in data[5].items():
                slc = QtCharts.QPieSlice(str(key), value) if year =='Overall' else QtCharts.QPieSlice(months[key-1], value)
                if value > 0: slc.setLabelVisible(True)
                slc.setExplodeDistanceFactor(0.05)
                slc.setBorderWidth(0)
                slc.setLabelFont((QtGui.QFont('Segoe MDL2 Assets', 10)))
                slc.setColor(QtGui.QColor(0,green,255))
                green += 15
                if green > 255: green = 200
                slc.setLabelPosition(QtCharts.QPieSlice.LabelPosition.LabelInsideNormal)
                slc.hovered.connect(lambda x, slc=slc, data=data: explode_slice(slc, data[0]))
                series.append(slc)

            pie_chart.addSeries(series)
            chart_view = QtCharts.QChartView(pie_chart)
            chart_view.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                     QtWidgets.QSizePolicy.Policy.Expanding)
            chart_view.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing | QtGui.QPainter.RenderHint.TextAntialiasing)
            gridLayout_mf.addWidget(chart_view, 0, 1, 1, 1)

            ###################################################################################

            # Rating frame
            rating_frame = QtWidgets.QFrame(main_frame)
            ratinglayout = QtWidgets.QHBoxLayout(rating_frame)
            avg_rate = QtWidgets.QLabel(rating_frame)

            rating_chart = self.create_bar(data[1])
            rating_chart.setMinimumSize(315, 150)

            avg_rate.setText(data[2] + '\nAvg')
            avg_rate.setObjectName('avg')

            ratinglayout.setSpacing(30)
            ratinglayout.addWidget(rating_chart)
            ratinglayout.addWidget(avg_rate)

            ###################################################################################

            # reviews, comments
            reviews_label = QtWidgets.QLabel(rating_frame)
            comments_label = QtWidgets.QLabel(rating_frame)
            if year=='Overall':
                comments_label.setText('<center>You wrote:<br>' + str(sum(comments.values())) + ' comments')
                reviews_label.setText('<center>You wrote:<br>' + str(sum(comments.values())) + '  reviews')
            else:
                if year not in comments: comments[year] = 0
                if year not in reviews: reviews[year] = 0
                comments_label.setText('<center>You wrote:<br>' + str(comments[year]) + ' comments')
                reviews_label.setText('<center>You wrote:<br>' + str(reviews[year]) + '  reviews')

            ratinglayout.addWidget(comments_label)
            ratinglayout.addWidget(reviews_label)

            gridLayout_mf.addWidget(rating_frame, 2, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)
            gridLayout_mf.addWidget(comments_label, 2, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)
            gridLayout_mf.addWidget(reviews_label, 2, 2, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)

            ###################################################################################

            # Api data if exists
            if data[-1]:
                geners_bar = self.create_bar(data[-1][0], True)
                countries_bar = self.create_bar(data[-1][1], True)

                geners_bar.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                              QtWidgets.QSizePolicy.Policy.Expanding)
                countries_bar.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                              QtWidgets.QSizePolicy.Policy.Expanding)

                gridLayout_mf.addWidget(countries_bar, 0, 2, 2, 1)
                gridLayout_mf.addWidget(geners_bar, 0, 0, 2, 1)

                film_time = QtWidgets.QLabel(main_frame)
                film_time.setText('<center>You spent time:<br>' + "{:.0f}".format(data[-1][2]/60) + ' hours')
                gridLayout_mf.addWidget(film_time, 1, 1, 1, 1)

            ###################################################################################

            # Tables if exists

            if data[3]:
                # Best table
                best_label = QtWidgets.QLabel(main_frame)
                best_label.setText('Top 5 highest rated films')
                best_label.setObjectName('table_label')
                best_table = create_table(data[3])

                # Worst table
                worst_label = QtWidgets.QLabel(main_frame)
                worst_label.setText('Top 5 lowest rated films')
                worst_label.setObjectName('table_label')
                worst_table = create_table(data[4])

                gridLayout_mf.addWidget(best_label, 3, 0, 1, 3, QtCore.Qt.AlignmentFlag.AlignCenter)
                gridLayout_mf.addWidget(best_table, 4, 0, 1, 3, QtCore.Qt.AlignmentFlag.AlignCenter)
                gridLayout_mf.addWidget(worst_label, 5, 0, 1, 3, QtCore.Qt.AlignmentFlag.AlignCenter)
                gridLayout_mf.addWidget(worst_table, 6, 0, 1, 3, QtCore.Qt.AlignmentFlag.AlignCenter)

            self.stacked.addWidget(main_frame)
        self.stacked.setCurrentIndex(len(films_by_year.keys())-1)

    def hovered(self, series):
        # i haven't found a way to interact with individual bar of a bar chart so it will display data for all bars
        if series.isLabelsVisible(): series.setLabelsVisible(False)
        else: series.setLabelsVisible(True)

    def create_bar(self, df, isvertical=False):

        self.bar_color = '#ed8e00' if self.bar_color != '#ed8e00' else '#06ad00'

        barchart = QtCharts.QChart()
        barset = QtCharts.QBarSet('default')
        axis = QtCharts.QBarCategoryAxis()
        barset.setBorderColor(QtGui.QColor(0,0,1))

        if not isvertical:
            bar_series = QtCharts.QBarSeries()
            bar_data = df
            bar_series.setBarWidth(1)
            barchart.addAxis(axis, QtCore.Qt.AlignmentFlag.AlignBottom)
            bar_series.setLabelsPosition(QtCharts.QBarSeries.LabelsPosition.LabelsOutsideEnd)
            barset.setColor(QtGui.QColor('#575957'))

            # make plot area slightly bigger to fit lables
            axisY = QtCharts.QValueAxis()
            axisY.setVisible(False)
            axisY.setRange(0, max(bar_data.values())*1.4)
            barchart.addAxis(axisY, QtCore.Qt.AlignmentFlag.AlignLeft)

        else:
            bar_series = QtCharts.QHorizontalBarSeries()
            if len(df) < 10:
                for i in range(10 - len(df)):
                    df['\0'*i] = 0
            bar_data = dict(sorted(df.items(), key=lambda item: item[1])[-10:])
            bar_series.setLabelsPosition(QtCharts.QBarSeries.LabelsPosition.LabelsCenter)
            barchart.addAxis(axis, QtCore.Qt.AlignmentFlag.AlignLeft)
            barset.setColor(QtGui.QColor(self.bar_color))

        axis.setLineVisible(False)
        axis.append(str(k) for k in bar_data.keys())
        axis.setLabelsColor(QtGui.QColor('white'))
        axis.setGridLineVisible(False)
        barset.append(list(bar_data.values()))
        barset.setLabelFont((QtGui.QFont('Segoe MDL2 Assets', 12)))
        bar_series.append(barset)
        barchart.addSeries(bar_series)

        if not isvertical: bar_series.attachAxis(axisY)

        barchart.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)
        barchart.setAnimationDuration(self.animation_duration)
        barchart.legend().setVisible(False)
        bar_series.hovered.connect(lambda x: self.hovered(bar_series))
        barchart.setMargins(QtCore.QMargins(-5,-5,-5,-5))
        barchart.setBackgroundRoundness(0)
        barchart.setBackgroundBrush(QtGui.QBrush(QtGui.QColor("transparent")))

        chart_view = QtCharts.QChartView(barchart)
        chart_view.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing | QtGui.QPainter.RenderHint.TextAntialiasing)
        return chart_view

    def save_key(self, state):
        sc = requests.get('https://api.themoviedb.org/3/search/movie?api_key=' + api_key + '&query=Memento')
        if state == 2 and len(self.form.text()) > 30 and sc.status_code == 200:
            with open('YourAPIKey.txt', 'w') as f:
                f.write(self.form.text().strip())

    def restart_with_key(self, api_key_new):
        global api_key
        api_key = api_key_new
        self.api_process_start()
        self.save_key(self.checkSave.checkState().value)
        self.form.setText('')

    def api_process_start(self):
        self.process = Api_process()
        self.process.start()
        self.process.update.connect(self.api_process_update)

    def api_process_update(self, args):
        global films_by_year, problems, comments, reviews
        if type(args) == str:
            self.problem_label.setText(args)
            self.problem_label.setObjectName('notKey') if len(args) == 19 else self.problem_label.setObjectName('Key')
        else:
            films_by_year, problems, comments, reviews = args
            if problems == 0:
                self.problem_label.setText('No errors occured\n with films.')
                self.problem_label.setObjectName('notProblem')
            else:
                self.problem_label.setText('Errors occured with\n' + str(problems) + ' films.')
                self.problem_label.setObjectName('Problem')
            self.gridLayout.addWidget(self.tmdb, 1, 1, 1, 1)

            self.draw_stacked()
        # for some reason if you do not hide frame it will double border size of hovered button
        self.side_frame.hide()
        self.setStyleSheet(style)
        self.side_frame.show()

    def eventFilter(self, obj, event):
        if obj is self.side_frame and event.type() == QtCore.QEvent.Type.Enter and  self.checkLock.checkState().value == 0:
            self.side_animation.setStartValue(10)
            self.side_animation.setEndValue(self.side_width)
            self.side_animation.start()
            return True
        elif obj is self.side_frame and event.type() == QtCore.QEvent.Type.Leave and  self.checkLock.checkState().value == 0:
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
        # just check to make sure api_key is valid
        sc = requests.get('https://api.themoviedb.org/3/search/movie?api_key=' + api_key + '&query=Memento')
        if sc.status_code != 200: self.update.emit("No valid key found!")
        else: self.update.emit(clean_data.main(api_key))


if __name__ == "__main__":
    import sys
    # import alternative_clean_data as clean_data
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

