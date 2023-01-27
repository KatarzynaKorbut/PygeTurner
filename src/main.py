import logging
import os
import sys
import tempfile
from pathlib import Path
from typing import Optional

from music21 import converter, environment, note

from note_finder import NoteFinder

if os.environ["VIRTUAL_ENV"]:
    virtual_env_path = Path(os.environ["VIRTUAL_ENV"])
    qt_plugins_path = virtual_env_path / "Lib/site-packages/PySide6/plugins"
    os.environ["QT_PLUGIN_PATH"] = str(qt_plugins_path)

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox

from ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        logging.basicConfig(level=logging.DEBUG)
        self.setupUi(self)
        self.note_finder: Optional[NoteFinder] = None

        self.open_sheet.triggered.connect(self.on_open_sheet_triggered)
        self.open_sound.triggered.connect(self.on_open_sound_triggered)
        self.set_musescore_path.triggered.connect(self.on_set_musescore_path_triggered)

    def on_open_sheet_triggered(self, s):
        logging.debug("on_open_sheet_triggered(%s)", s)
        file_name, _ = QFileDialog.getOpenFileName(
            self, caption="Otwórz nuty", filter="MusicXML (*.mxl)"
        )
        if file_name:
            logging.info("Loading sheet music from %s", file_name)
            try:
                music_stream = converter.parse(file_name)
                sheet_pixmap = self.music_to_pixmap(music_stream)
            except Exception as ex:
                logging.exception("Failed to load %s", file_name)
                QMessageBox(self).critical(
                    self,
                    "PygeTurner",
                    f"Nie można załadować pliku:\n{ex}",
                    QMessageBox.StandardButton.Ok,
                )
            else:
                self.sheet_view.load(sheet_pixmap)
                sheet_notes = [
                    n for n in music_stream.recurse().notes if isinstance(n, note.Note)
                ]
                logging.debug("Number of notes: %s", len(sheet_notes))
                self.note_finder = NoteFinder(sheet_notes)

    def music_to_pixmap(self, music_stream):
        conv = converter.subConverters.ConverterMusicXML()
        with tempfile.TemporaryDirectory(prefix="PygeTurner-") as tmp_dir:
            # if tmp_dir:= tempfile.mkdtemp(prefix="PygeTurner-"):
            tmp_path = Path(tmp_dir) / "PygeTurner"
            image_path = conv.write(
                music_stream,
                fmt="musicxml",
                fp=str(tmp_path),
                subformats=["png"],
            )
            logging.debug("Sheet image file: %s", image_path)
            return QPixmap(str(image_path))

    def on_open_sound_triggered(self, s):
        file_path, _ = QFileDialog.getOpenFileName(
            self, caption="Otwórz dźwięk", filter="Pliki WAV (*.wav)"
        )
        if file_path:
            logging.debug("Loading sound from %s", file_path)
            self.audio_player.load(file_path)

    def on_set_musescore_path_triggered(self, s):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            caption="Znajdź program MuseScore3.exe",
            filter="Program MuseScore3 (*.exe)",
        )
        if file_path:
            logging.debug("Setting musescoreDirectPNGPath to %s", file_path)
            music21_settings = environment.UserSettings()
            music21_settings["musescoreDirectPNGPath"] = file_path


app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
