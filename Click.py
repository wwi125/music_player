from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import pyqtSignal,Qt

class Slider_events(QSlider):
    Mouse_click = pyqtSignal(int)
    def __init__(self,Parent=None):
        super().__init__(Qt.Horizontal,Parent)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        value = event.localPos().x()
        self.setValue(round(value / self.width() * self.maximum()))
        self.Mouse_click.emit(value)
