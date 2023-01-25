from pathlib import Path
import sys
import tempfile
import logging

from PySide6 import QtWidgets, QtGui, QtMultimedia
from ui_main_window import Ui_MainWindow
from music21 import converter, environment, note, stream


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        logging.basicConfig(level=logging.DEBUG)
        self.setupUi(self)

        self.setup_sheet_viewer()
        self.open_sheet.triggered.connect(self.on_open_sheet_triggered)

        self.open_sound.triggered.connect(self.on_open_sound_triggered)

        self.setup_player()

        self.on_play_pause_button_toggled(False)
        self.play_pause_button.toggled.connect(self.on_play_pause_button_toggled)

    def setup_player(self):
        self.audio_output = QtMultimedia.QAudioOutput(self)
        self.player = QtMultimedia.QMediaPlayer(self)
        self.player.setAudioOutput(self.audio_output)
        self.player.durationChanged.connect(self.player_duration_changed)
        self.player.positionChanged.connect(self.player_position_changed)
        self.player.playbackStateChanged.connect(self.player_playback_state_changed)
        self.player_duration = 0
        self.player_position = 0
        # self.time_slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        # self.time_slider.setTickInterval(1000)
        self.time_slider.valueChanged.connect(self.time_slider_changed)
        self.time_slider.sliderReleased.connect(self.time_slider_released)

    def on_play_pause_button_toggled(self, is_checked):
        logging.debug("on_play_pause_button_clicked %s", is_checked)
        style = self.style()
        if is_checked:
            self.play_pause_button.setIcon(
                QtGui.QIcon.fromTheme(
                    "media-playback-pause.png",
                    style.standardIcon(QtWidgets.QStyle.StandardPixmap.SP_MediaPause),
                )
            )
            self.player.play()
        else:
            self.play_pause_button.setIcon(
                QtGui.QIcon.fromTheme(
                    "media-playback-start.png",
                    style.standardIcon(QtWidgets.QStyle.StandardPixmap.SP_MediaPlay),
                )
            )
            self.player.pause()

    def setup_sheet_viewer(self):
        self.sheet_scene = QtWidgets.QGraphicsScene(self.sheet_view)
        self.sheet_pixmap_item = QtWidgets.QGraphicsPixmapItem()
        self.sheet_scene.addItem(self.sheet_pixmap_item)
        self.sheet_view.setScene(self.sheet_scene)
        self.sheet_view.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

    def on_open_sheet_triggered(self, s):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, caption="Otwórz nuty", filter="MusicXML (*.mxl)"
        )
        if file_name:
            self.load_sheet_music(file_name)

    def load_sheet_music(self, path):
        logging.info("Loading sheet music from %s", path)
        try:
            self.music_stream = converter.parse(path)
        except Exception as ex:
            logging.exception("Failed to load %s", path)
            QtWidgets.QMessageBox(self).critical(
                self,
                "PygeTurner",
                f"Nie można załadować pliku:\n{ex}",
                QtWidgets.QMessageBox.StandardButton.Ok,
            )
        else:
            logging.debug("%s", self.music_stream)
            conv = converter.subConverters.ConverterLilypond()
            with tempfile.TemporaryDirectory(prefix="PygeTurner-") as tmp_dir:
                # if tmp_dir:= tempfile.mkdtemp(prefix="PygeTurner-"):
                tmp_path = Path(tmp_dir) / "PygeTurner"
                image_path = conv.write(
                    self.music_stream,
                    fmt="musescore",
                    fp=str(tmp_path),
                    subformats=["png"],
                )
                logging.debug("Sheet image file: %s", image_path)
                pixmap = QtGui.QPixmap(str(image_path))
                self.sheet_pixmap_item.setPixmap(pixmap)
                rect = pixmap.rect()
                logging.debug("Sheet image size: %s", rect)
                self.sheet_view.setSceneRect(rect)

    def on_open_sound_triggered(self, s):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, caption="Otwórz dźwięk", filter="Pliki WAV (*.wav)"
        )
        if file_name:
            logging.debug("Loading sound from %s", file_name)
            self.play_pause_button.setEnabled(True)
            self.time_slider.setEnabled(True)
            self.player.setSource(file_name)

    @staticmethod
    def time_to_text(milliseconds: int) -> str:
        hours = milliseconds // (1000 * 3600)
        milliseconds -= hours * (1000 * 3600)
        minutes = milliseconds // (1000 * 60)
        milliseconds -= minutes * (1000 * 60)
        seconds = milliseconds // 1000
        milliseconds -= seconds * 1000
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def update_timer(self):
        self.time_label.setText(
            f"{self.time_to_text(self.player_position)}"
            " / "
            f"{self.time_to_text(self.player_duration)}"
        )

    def player_position_changed(self, milliseconds: int):
        if not self.time_slider.isSliderDown():
            self.player_position = milliseconds
            self.update_timer()
            self.time_slider.setSliderPosition(milliseconds)

    def player_duration_changed(self, milliseconds: int):
        logging.debug("Media duration: %s", milliseconds)
        self.player_duration = milliseconds
        self.update_timer()
        self.time_slider.setMaximum(milliseconds)

    def player_playback_state_changed(self, state: QtMultimedia.QMediaPlayer.PlaybackState):
        logging.debug("Player playback state changed: %s", state)
        if state == QtMultimedia.QMediaPlayer.PlaybackState.StoppedState:
            self.play_pause_button.toggle()

    def time_slider_changed(self, position):
        if self.time_slider.isSliderDown():
            logging.debug("Time slider position: %s", position)
            self.player_position = position
            self.update_timer()
            self.time_slider.setSliderPosition(position)

    def time_slider_released(self):
        self.player.setPosition(self.player_position)


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
