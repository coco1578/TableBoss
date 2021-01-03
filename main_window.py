import sys
import time
import threading

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *

from sub_window import ResolutionInputDialog

PROGRESSBAR_DEFAULT_STYLE = """
                QProgressBar::chunk {
                background-color: orange;
                width: 10px;
                margin: 1px;
                }
                """
PUSHBUTTON_DEFAULT_PLAY_STYLE = """
                QPushButton {
                image: url(./img/play_button);
                border: 0px;
                }
                """
PUSHBUTTON_DEFAULT_PAUSE_STYLE = """
                QPushButton {
                image: url(./img/pause_button);
                border: 0px;
                }
                """


class MainWindow(QMainWindow):
    EXIT_CODE_REBOOT = -9999

    def __init__(self, master=None):
        super().__init__()

        self.setWindowTitle('Table Boss Timer')

        self.blind_level = 1
        self.is_started = False
        self.ss_button_show = True
        # self.time_value = "00:00"

        # For test purpose, after add menu bar then I'll remove it
        self.m = 1
        self.t = 0
        self.tt = self.m * 60 + self.t
        self.time_value = "{:02d}:{:02d}".format(self.m, self.t)
        self.is_running = threading.Event()
        # self.timer_thread = threading.Thread(target=self.tick_tock)
        # self.prograss_bar_thread = threading.Thread(target=self.update_prograss_bar)

        self._create_ui()

    def _create_ui(self):

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.v_box_layout = QVBoxLayout()

        self.title_layout = QVBoxLayout()
        self.title = QLabel()
        self.title.setText("Table Boss Timer")
        self.title.setFont(QtGui.QFont('Arial', 70))
        # TODO: Font Size, Font Style, etc..
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title_layout.addWidget(self.title)
        self.v_box_layout.addLayout(self.title_layout) # Add title layout to v box layout

        self.timer_layout = QVBoxLayout()
        self.blind_level_label = QLabel()
        self.blind_level_label.setText("LV %d" % self.blind_level)
        self.blind_level_label.setFont(QtGui.QFont('Arial', 90))
        self.blind_level_label.setAlignment(QtCore.Qt.AlignCenter)
        self.time_label = QLabel()
        self.time_label.setText(self.time_value)
        self.time_label.setFont(QtGui.QFont('Arial', 300))
        self.time_label.setAlignment(QtCore.Qt.AlignCenter)
        self.timer_layout.addStretch(1)
        self.timer_layout.addWidget(self.blind_level_label)
        self.timer_layout.addWidget(self.time_label)
        # TODO: Will be add Prograss bar in the center of the Timer
        # self.timer_prograss_bar = QProgressBar()
        # self.timer_prograss_bar.setTextVisible(False)
        # self.timer_prograss_bar.setStyleSheet(PROGRESSBAR_DEFAULT_STYLE)
        # self.timer_prograss_bar.setValue(0)
        # self.timer_layout.addWidget(self.timer_prograss_bar)
        self.blind_layout = QHBoxLayout()
        self.small_blind_layout = QVBoxLayout()
        self.small_blind_label = QLabel()
        self.small_blind_label.setText("Small Blind")
        self.small_blind_label.setFont(QtGui.QFont('Arial', 60))
        self.small_blind_label.setAlignment(QtCore.Qt.AlignCenter)
        self.small_blind_time = QLabel()
        self.small_blind_time.setText("1")
        self.small_blind_time.setFont(QtGui.QFont('Arial', 120))
        self.small_blind_time.setAlignment(QtCore.Qt.AlignCenter)
        self.small_blind_layout.addWidget(self.small_blind_label)
        self.small_blind_layout.addWidget(self.small_blind_time)
        self.blind_layout.addLayout(self.small_blind_layout)
        self.big_blind_layout = QVBoxLayout()
        self.big_blind_label = QLabel()
        self.big_blind_label.setText("Big Blind")
        self.big_blind_label.setFont(QtGui.QFont('Arial', 60))
        self.big_blind_label.setAlignment(QtCore.Qt.AlignCenter)
        self.big_blind_time = QLabel()
        self.big_blind_time.setText("2")
        self.big_blind_time.setFont(QtGui.QFont('Arial', 120))
        self.big_blind_time.setAlignment(QtCore.Qt.AlignCenter)
        self.big_blind_layout.addWidget(self.big_blind_label)
        self.big_blind_layout.addWidget(self.big_blind_time)
        # self.big_blind_layout.addStretch(1)
        self.blind_layout.addLayout(self.big_blind_layout)
        self.timer_layout.addLayout(self.blind_layout)
        self.timer_layout.addStretch(1)

        self.button_layout = QHBoxLayout()
        self.start_and_stop_button = QPushButton()
        self.start_and_stop_button.setText("Start")
        self.start_and_stop_button.setFont(QtGui.QFont('Arial', 30))
        # TODO: Add Backgorund Image in Button
        # self.start_and_stop_button.setStyleSheet(PUSHBUTTON_DEFAULT_PLAY_STYLE)
        self.start_and_stop_button.clicked.connect(self.button_click_event)
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.start_and_stop_button)
        self.button_layout.addStretch(1) # 박스의 주위에 공간을 미리 할당하여 위치를 고정시키는 것

        self.v_box_layout.addLayout(self.timer_layout)
        self.v_box_layout.addLayout(self.button_layout)

        self.main_widget.setLayout(self.v_box_layout)

        # menu bar usage
        self.menu_bar = QMenuBar(self)
        self.menu_bar.setNativeMenuBar(False)

        # Program Menu - Restart / Exit ..
        self.menu_file = QMenu('Program', self.menu_bar)
        self.menu_file.setObjectName("menu_file")

        # self.file_action_open = QAction('Open', self)
        # self.file_action_open.setObjectName('open_action')
        # self.file_action_open.setShortcut('Ctrl+O')
        # self.file_action_open.setStatusTip('Open config file.')
        # TODO: Add open directory funciton.
        # self.file_action_open.triggered.connect(self.open_dir)

        self.file_action_restart = QAction('Restart', self)
        self.file_action_restart.setObjectName("restart_action")
        self.file_action_restart.setShortcut('Ctrl+R')
        self.file_action_restart.setStatusTip('Restart Program.')
        self.file_action_restart.triggered.connect(self._restart)

        self.file_action_exit = QAction('Exit', self)
        self.file_action_exit.setObjectName("exit_action")
        if sys.platform == 'win32':
            self.file_action_exit.setShortcut('Alt+F4')
        elif sys.platform == 'darwin':
            self.file_action_exit.setShortcut('Ctrl+Q')
        self.file_action_exit.setStatusTip('Exit Application.')
        self.file_action_exit.triggered.connect(self.close)
        self.file_action_exit.setStatusTip('Exit application')

        # self.menu_file.addAction(self.file_action_open)
        self.menu_file.addAction(self.file_action_restart)
        self.menu_file.addAction(self.file_action_exit)

        # View Menu - Resolution
        # self.menu_view = QMenu('View', self.menu_bar)
        # self.menu_view.setObjectName('menu_view')
        # self.view_resolution = QMenu('Resolution', self)
        # self.view_resolution.setObjectName("resolution_action")
        #
        # self.view_resolution_fhd = QAction('FHD', self, checkable=True)
        # self.view_resolution_fhd.setObjectName('fhd')
        # self.view_resolution_fhd.triggered.connect(self._change_resolution)
        #
        # self.view_resolution_add = QAction('Add Resolution', self)
        # self.view_resolution_add.setObjectName('add_resolution')
        # self.view_resolution_add.triggered.connect(self._add_resolution)
        #
        # self.view_resolution.addAction(self.view_resolution_fhd)
        # self.view_resolution.addAction(self.view_resolution_add)
        # self.menu_view.addAction(self.view_resolution.menuAction())

        # Help Menu - Contact
        self.menu_help = QMenu('Help', self.menu_bar)
        self.menu_help.setObjectName('menu_help')
        self.help_contact_me = QAction('Contact', self)
        self.help_contact_me.setObjectName('contact_me')
        self.help_contact_me.triggered.connect(self._contact_me)
        self.menu_help.addAction(self.help_contact_me)

        self.setMenuBar(self.menu_bar)
        self.menu_bar.addAction(self.menu_file.menuAction())
        # self.menu_bar.addAction(self.menu_view.menuAction())
        self.menu_bar.addAction(self.menu_help.menuAction())

        # cp = QDesktopWidget().availableGeometry()
        # print(cp)
        # self.setGeometry(0, 0, 1920, 1080)
        # self.setGeometry(cp)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        pass
        # print("pressed") # For debug

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:

        if self.ss_button_show is True:
            self.start_and_stop_button.hide()
            self.ss_button_show = False
        else:
            self.start_and_stop_button.show()
            self.ss_button_show = True

        # print("released") # For debug

    def button_click_event(self):

        if self.is_started is False:
            self.start_and_stop_button.setText("Stop")
            self.is_started = True
            self.start_and_stop_button.hide()
            self.ss_button_show = False
            self.is_running.clear()
            threading.Thread(target=self.tick_tock).start()
            # self.prograss_bar_thread.start()
            # self.start_and_stop_button.setStyleSheet(PUSHBUTTON_DEFAULT_PAUSE_STYLE)
        else:
            self.start_and_stop_button.setText("Start")
            self.is_started = False
            self.start_and_stop_button.hide()
            self.ss_button_show = False
            self.is_running.set()
            # self.start_and_stop_button.setStyleSheet(PUSHBUTTON_DEFAULT_PLAY_STYLE)

    def set_up(self):

        self.m = 3
        self.t = 0
        self.tt = self.m * 60 + self.t
        self.time_value = "{:02d}:{:02d}".format(self.m, self.t) # after make menu bar the variable name going to be self.time_value
        self.time_label.setText(self.time_value)

    def tick_tock(self):
        while not self.is_running.is_set():

            if self.tt == 0:
                self.tt = self.m * 60 + self.t
                self.time_value = "{:02d}:{:02d}".format(self.m, self.t)
                self.blind_level += 1
                self.blind_level_label.setText("LV %d" % self.blind_level)

            time.sleep(1)
            self.time_value = self.time_value.split(":")

            if int(self.time_value[1]) == 0: # 3:00 - 1
                minute = int(self.time_value[0]) - 1
                second = 59
                self.time_value = "{:02d}:{:02d}".format(minute, second)
                self.time_label.setText(self.time_value)
            else:
                minute = int(self.time_value[0])
                second = int(self.time_value[1]) - 1
                self.time_value = "{:02d}:{:02d}".format(minute, second)
                self.time_label.setText(self.time_value)

            self.tt = self.tt - 1

    def _add_resolution(self):
        self.custom = 0
        input_dialog = ResolutionInputDialog()
        if input_dialog.exec():
            width, height = input_dialog.get_resolution()
        width, height = int(width), int(height)
        if not int(width) > 0 and int(height) > 0:
            # Add Error handling (May be message box)
            pass
        else:
            self.view_resolution_custom = QAction('%dX%d' % (width, height), self, checkable=True)
            self.view_resolution_custom.setObjectName('%dX%d' % (width, height))
            self.view_resolution_custom.triggered.connect(self._change_resolution)
            self.view_resolution.addAction(self.view_resolution_custom)

    def _change_resolution(self):

        if self.view_resolution_fhd.isChecked():
            monitor_geometry = QDesktopWidget().availableGeometry()
            x = monitor_geometry.x()
            y = monitor_geometry.y()
            w = 1920
            h = 1080
            self.setGeometry(x, y, w, h)
        elif self.view_resolution_custom.isChecked():
            object_name = str(self.view_resolution_custom.objectName())
            print(object_name)

    def _contact_me(self):

        self.msg_box = QMessageBox()
        self.msg_box.setWindowTitle('Contact Me')
        self.msg_box.setText('Contact\nName: Coco Kim\nEmail: rlawnsgh0826@gmail.com')
        self.msg_box.exec_()

    def _restart(self):
        self.is_running.set()
        time.sleep(1) # Wait for thread is finished
        QApplication.exit(self.EXIT_CODE_REBOOT)

    # def update_prograss_bar(self):
    #
    #     count = 0
    #     self.prograss_bar_sleep_time = self.tt / 100
    #     while not self.is_running.is_set():
    #         if self.tt == 0 or count == 100:
    #             self.timer_prograss_bar.setValue(0)
    #         time.sleep(self.prograss_bar_sleep_time)
    #         count += 1
    #         self.timer_prograss_bar.setValue(count)


def main():

    exit_code = MainWindow.EXIT_CODE_REBOOT
    print(exit_code)
    while exit_code == MainWindow.EXIT_CODE_REBOOT:
        app = QApplication(sys.argv)
        p = MainWindow()
        p.show()
        exit_code = app.exec()
        print(exit_code)
        app = None


if __name__ == '__main__':

    main()