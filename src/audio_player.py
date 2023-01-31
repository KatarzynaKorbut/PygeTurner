import logging

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import QHBoxLayout, QLabel, QSlider, QStyle, QToolButton, QWidget


class AudioPlayer(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._layout_wigdets()

        self.player_duration = 0
        self.player_position = 0

        self.audio_output = QAudioOutput(self)
        self.player = QMediaPlayer(self)
        self.player.setAudioOutput(self.audio_output)

        self.player.durationChanged.connect(self._player_duration_changed)
        self.player.positionChanged.connect(self._player_position_changed)
        self.player.playbackStateChanged.connect(self._player_playback_state_changed)
        self.time_slider.valueChanged.connect(self._time_slider_changed)
        self.time_slider.sliderReleased.connect(self._time_slider_released)
        self.play_pause_button.toggled.connect(self._on_play_pause_button_toggled)

        self._on_play_pause_button_toggled(False)

    def _layout_wigdets(self):
        audio_player_layout = QHBoxLayout(self)
        audio_player_layout.setObjectName("audio_player_layout")

        self.play_pause_button = QToolButton(self)
        self.play_pause_button.setObjectName("play_pause_button")
        self.play_pause_button.setEnabled(False)
        self.play_pause_button.setCheckable(True)
        audio_player_layout.addWidget(self.play_pause_button)

        self.time_slider = QSlider(self)
        self.time_slider.setObjectName("time_slider")
        self.time_slider.setEnabled(False)
        self.time_slider.setOrientation(Qt.Orientation.Horizontal)
        # self.time_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        # self.time_slider.setTickInterval(1000)
        audio_player_layout.addWidget(self.time_slider)

        self.time_label = QLabel(self)
        self.time_label.setObjectName("time_label")
        self.time_label.setText("00:00:00 / 00:00:00")
        audio_player_layout.addWidget(self.time_label)

    def load(self, file_path):
        self.play_pause_button.setEnabled(True)
        self.time_slider.setEnabled(True)
        self.player.setSource(file_path)

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

    def is_playing(self):
        return self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState

    def _player_duration_changed(self, milliseconds: int):
        logging.debug("Media duration: %s ms", milliseconds)
        self.player_duration = milliseconds
        self.update_timer()
        self.time_slider.setMaximum(milliseconds)

    def _player_position_changed(self, milliseconds: int):
        if not self.time_slider.isSliderDown():
            self.player_position = milliseconds
            self.update_timer()
            self.time_slider.setSliderPosition(milliseconds)

    def _player_playback_state_changed(self, state: QMediaPlayer.PlaybackState):
        logging.debug("Player playback state changed: %s", state)
        if state == QMediaPlayer.PlaybackState.StoppedState:
            self.play_pause_button.setDown(False)

    def _time_slider_changed(self, position):
        if self.time_slider.isSliderDown():
            logging.debug("Time slider position: %s", position)
            self.player_position = position
            self.update_timer()
            self.time_slider.setSliderPosition(position)

    def _time_slider_released(self):
        self.player.setPosition(self.player_position)

    def _on_play_pause_button_toggled(self, is_checked):
        logging.debug("on_play_pause_button_clicked %s", is_checked)
        if is_checked:
            self.play_pause_button.setIcon(
                QIcon.fromTheme(
                    "media-playback-pause.png",
                    self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause),
                )
            )
            self.player.play()
        else:
            self.play_pause_button.setIcon(
                QIcon.fromTheme(
                    "media-playback-start.png",
                    self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay),
                )
            )
            self.player.pause()
