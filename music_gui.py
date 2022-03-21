from PyQt5 import QtCore,QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon,QPixmap,QPainter,QPainterPath
from Click import Slider_events

class music_ui(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(1130, 590)
        MainWindow.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.music_image = 'images/02pdxQ8bp9.png'
        self.Menu(MainWindow)
        self.all_layout(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def Menu(self,MainWindow):
            # ----------菜单栏----------
            self.menubar = QtWidgets.QMenuBar(MainWindow)
            self.menubar.setGeometry(QtCore.QRect(0, 0, 1130, 26))
            self.menubar.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
            self.menu_music = self.menubar.addMenu('&文件')
            # ----------打开文件和文件夹----------
            self.Open_ = QtWidgets.QMenu('打开')
            self.Open_file = QtWidgets.QAction('打开文件')
            self.Open_file.setShortcut('Ctrl+O')
            self.Open_folder = QtWidgets.QAction('打开文件夹')
            self.Open_.addAction(self.Open_file)
            self.Open_.addAction(self.Open_folder)
            self.menu_music.addMenu(self.Open_)
            # ----------退出程序----------
            self.exit = QtWidgets.QAction('退出')
            self.exit.setShortcut('Ctrl+Q')
            self.menu_music.addAction(self.exit)


    def all_layout(self,MainWindow):
        self.Play_control_button = QtWidgets.QPushButton()
        self.Sound_button = QtWidgets.QPushButton()
        self.Previous_button = QtWidgets.QPushButton()
        self.Next_button = QtWidgets.QPushButton()
        self.Mode_button = QtWidgets.QPushButton()
        self.Volume = QtWidgets.QSlider()
        self.Progress = Slider_events()
        self.Play_control_button.setIcon(QIcon('images/play.png'))
        self.Sound_button.setIcon(QIcon('images/sound_on.png'))
        self.Previous_button.setIcon(QIcon('images/previous.png'))
        self.Next_button.setIcon(QIcon('images/next.png'))
        self.Mode_button.setIcon(QIcon('images/list_loop.png'))
        self.Volume.setRange(0, 100)
        self.Volume.setValue(100)
        self.Volume.setOrientation(Qt.Horizontal)
        self.Progress.setEnabled(False)
        self.Progress.setMinimum(0)
        self.Progress.setOrientation(Qt.Horizontal)
        self.time = QtWidgets.QLabel()
        self.time.setText('00:00/00:00')
        # ----------布局----------
        all_layout = QtWidgets.QHBoxLayout()
        h1_layout = QtWidgets.QHBoxLayout()
        h2_layout = QtWidgets.QVBoxLayout()
        #----------左侧
        left = QtWidgets.QHBoxLayout()
        self.listwidget = QtWidgets.QListWidget()
        self.listwidget.setMaximumHeight(500)
        self.listwidget.setMaximumWidth(500)
        left.addWidget(self.listwidget)
        #----------右侧
        right = QtWidgets.QHBoxLayout()
        self.lbabel = QtWidgets.QLabel()
        self.lbabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.Image(self.music_image)
        right.addWidget(self.lbabel)
        #----------底层
        underlay = QtWidgets.QVBoxLayout()
        underlay_h1 = QtWidgets.QHBoxLayout()
        underlay_h2 = QtWidgets.QHBoxLayout()
        underlay_h1.addWidget(self.Progress)
        underlay_h1.addWidget(self.time)
        underlay_h2.addStretch(1)
        underlay_h2.addWidget(self.Mode_button)
        underlay_h2.addWidget(self.Previous_button)
        underlay_h2.addWidget(self.Play_control_button)
        underlay_h2.addWidget(self.Next_button)
        underlay_h2.addWidget(self.Sound_button)
        underlay_h2.addWidget(self.Volume)
        underlay_h2.addStretch(1)
        underlay.addStretch(1)
        underlay.addLayout(underlay_h1)
        underlay.addLayout(underlay_h2)
        #----------
        h1_layout.addLayout(left)
        h2_layout.addStretch(2)
        h2_layout.addLayout(right)
        h2_layout.addStretch(2)
        h2_layout.addLayout(underlay)
        all_layout.addLayout(h1_layout)
        all_layout.addLayout(h2_layout)
        self.centralwidget.setLayout(all_layout)
        MainWindow.setCentralWidget(self.centralwidget)

    def Image(self, music_image):
        self.p_image = QPixmap(music_image).scaled(350, 350, Qt.KeepAspectRatioByExpanding,Qt.SmoothTransformation)
        self.pixmap = QPixmap(350, 350)
        self.pixmap.fill(Qt.transparent)
        self.painter = QPainter(self.pixmap)
        self.painter.begin(self)
        self.painter.setRenderHint(QPainter.Antialiasing, True)
        self.painter.setRenderHints(QPainter.SmoothPixmapTransform, True)
        self.painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        self.path = QPainterPath()
        self.path.addEllipse(0, 0, 350, 350)
        self.painter.setClipPath(self.path)
        self.painter.drawPixmap(0, 0, 350, 350, self.p_image)
        self.painter.end()
        self.lbabel.setPixmap(self.pixmap)