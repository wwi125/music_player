import os.path
import sys
from PyQt5.QtWidgets import QFileDialog,qApp,QMainWindow,QApplication
from PyQt5.QtMultimedia import QMediaPlayer,QMediaContent, QMediaPlaylist
from PyQt5.QtCore import QUrl,QDateTime
from PyQt5.QtGui import QIcon
from mutagen import File
from music_gui import music_ui



class music_player(QMainWindow,music_ui):
    def __init__(self):
        super(music_player, self).__init__()
        self.setupUi(self)
        self.music_list = QMediaPlaylist()
        self.player = QMediaPlayer()
        self.player.setPlaylist(self.music_list)
        self.mode = 'Loop'
        self.music_list.setPlaybackMode(QMediaPlaylist.Loop)
        self.image = 'images/02pdxQ8bp9.png'
        self.Open_file.triggered.connect(self.op_finame)
        self.Open_folder.triggered.connect(self.op_folder)
        self.exit.triggered.connect(self.quit)
        self.Play_control_button.clicked.connect(self.play_n_pause)
        self.Sound_button.clicked.connect(self.Volume_switch)
        self.Volume.valueChanged.connect(self.Volume_slider)
        self.Previous_button.clicked.connect(self.prev_music)
        self.Next_button.clicked.connect(self.next_music)
        self.Mode_button.clicked.connect(self.playmode)
        self.player.positionChanged.connect(self.get_time)
        self.Progress.setValue(0)
        self.Progress.setMinimum(0)
        self.Progress.sliderMoved.connect(self.change_time)
        self.Progress.Mouse_click.connect(self.clicked_time)
        self.listwidget.itemClicked.connect(self.list_play_func)

    def op_finame(self):    #打开文件
        finame,filetype=QFileDialog.getOpenFileNames(self, "打开文件", "E:\\","*.mp3;*.flac;*.wav" )
        for song in finame:
            path = QUrl.fromLocalFile(song)
            self.music_list.addMedia(QMediaContent(path))
            self.listwidget.addItem(song.split('/')[-1])


    def op_folder(self):    #打开文件夹
        song_formats = ['mp3', 'flac', 'wav']
        folder=QFileDialog.getExistingDirectory(self,"打开文件夹","E:\\")
        try:
            for song in os.listdir(folder):
                    if song.split('.')[-1] in song_formats:
                        path = QUrl.fromLocalFile(os.path.join(folder, song))
                        self.music_list.addMedia(QMediaContent(path))
                        self.listwidget.addItem(song)
        except OSError as e:
            return


    def quit(self):     #退出
        exit = qApp.quit()


    def play_n_pause(self):     #播放和暂停音乐
        if self.player.state() == 1:
            self.player.pause()
            self.Play_control_button.setIcon(QIcon('images/play.png'))
        else:
            self.player.play()
            self.Play_control_button.setIcon(QIcon('images/pause.png'))


    def prev_music(self):       #上一首
        if self.music_list.currentIndex() == 0:
            self.music_list.setCurrentIndex(self.music_list.mediaCount() - 1)
            self.music_Image()
        else:
            self.music_list.previous()
            self.music_Image()


    def next_music(self):       #下一首
        if self.music_list.currentIndex() == self.music_list.mediaCount() - 1:
            self.music_list.setCurrentIndex(0)
            self.music_Image()
        else:
            self.music_list.next()
            self.music_Image()


    def playmode(self):     #切换播放模式
        if self.mode == 'Loop':
            self.mode = 'Random'
            self.Mode_button.setIcon(QIcon('images/random.png'))
            self.music_list.setPlaybackMode(QMediaPlaylist.Random)
        elif self.mode == 'Random':
            self.mode = 'CurrentItemInLoop'
            self.Mode_button.setIcon(QIcon('images/item_loop.png'))
            self.music_list.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
        elif self.mode == 'CurrentItemInLoop':
            self.mode = 'Loop'
            self.Mode_button.setIcon(QIcon('images/list_loop.png'))
            self.music_list.setPlaybackMode(QMediaPlaylist.Loop)

    def Volume_switch(self):   #点击按钮音量开关
        if self.player.isMuted():
            self.player.setMuted(False)
            self.Sound_button.setIcon(QIcon('images/sound_on'))
        else:
            self.player.setMuted(True)
            self.Sound_button.setIcon(QIcon('images/sound_off'))

    def Volume_slider(self,value):    #判断音量大小而开关
        self.player.setVolume(value)
        if value == 0:
            self.Sound_button.setIcon(QIcon('images/sound_off'))
        else:
            self.Sound_button.setIcon(QIcon('images/sound_on'))

    def list_play_func(self):       #列表播放
        list = self.listwidget.currentRow()
        self.music_list.setCurrentIndex(list)
        self.music_Image()
        self.player.play()
        self.Play_control_button.setIcon(QIcon('images/pause.png'))
        self.Progress.setEnabled(True)


    def get_time(self,num): #进度条
        self.Progress.setMaximum(self.player.duration())
        self.Progress.setEnabled(True)
        self.Progress.setValue(num)
        time = QDateTime.fromMSecsSinceEpoch(num).toString("mm:ss")
        all_time = QDateTime.fromMSecsSinceEpoch(self.player.duration()).toString("mm:ss")
        self.time.setText(time + '/' + all_time)
        if time == all_time:
            self.music_Image()

    def change_time(self):  #拖动进度条
        self.player.setPosition(round(self.Progress.value()*self.player.duration()/self.Progress.maximum()))

    def clicked_time(self): #点击进度条
        self.player.setPosition(round(self.Progress.value()*self.player.duration()/self.Progress.maximum()))

    def music_Image(self): #提取专辑图片
        load =  self.player.currentMedia().canonicalUrl().path()
        path = load.replace('/','',1)
        if '.flac' in path:
            var = File(path)
            pics = var.pictures
            # print(pics)
            if 'image' in str(pics):
                for p in pics:
                    if p.type == 3:
                        with open('images/cover.jpg', 'wb') as f:
                            f.write(p.data)
                music_image = 'images/cover.jpg'
                self.Image(music_image)
            else:
                music_image = 'images/02pdxQ8bp9.png'
                self.Image(music_image)
        elif '.mp3' in path:
            var = File(path)
            if 'APIC' in str(var):
                pics = var.tags['APIC:'].data
                with open('images/cover.jpg', 'wb') as f:
                    f.write(pics)
                music_image = 'images/cover.jpg'
                self.Image(music_image)
            else:
                music_image = 'images/02pdxQ8bp9.png'
                self.Image(music_image)
        elif '.wav' in path:
            music_image = 'images/02pdxQ8bp9.png'
            self.Image(music_image)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = music_player()
    win.show()
    sys.exit(app.exec())