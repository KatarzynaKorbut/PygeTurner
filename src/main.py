import logging
import os
import sys
import tempfile
from pathlib import Path
from typing import Optional

from music21 import converter, environment
from music21.note import Note

from note_finder import NoteFinder
from transcriber import Transcriber

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
        logging.basicConfig(level=logging.INFO)
        self.setupUi(self)
        self.note_finder: Optional[NoteFinder] = None
        self.transcriber = Transcriber()

        self.open_sheet.triggered.connect(self.on_open_sheet_triggered)
        self.open_sound.triggered.connect(self.on_open_sound_triggered)
        self.set_musescore_path.triggered.connect(self.on_set_musescore_path_triggered)
        self.audio_player.player.positionChanged.connect(
            self.on_player_position_changed
        )

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
                sheet_notes = music_stream.recurse().getElementsByClass(Note)
                logging.debug("Number of notes: %s", len(sheet_notes))
                self.note_finder = NoteFinder(sheet_notes)

                lowest_note: Note = min(sheet_notes, key=lambda n: n.pitch.ps)
                highest_note: Note = max(sheet_notes, key=lambda n: n.pitch.ps)
                self.transcriber.set_note_range(
                    lowest_note.pitch.ps, highest_note.pitch.ps
                )
                self.open_sound.setEnabled(True)

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
            self.transcriber.load(file_path)

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

    def on_player_position_changed(self, milliseconds: int):
        if self.audio_player.is_playing():
            self.transcriber.update_time(milliseconds / 1000)
            if self.transcriber.has_new_note:
                new_note = self.transcriber.get_new_note()
                assert self.note_finder
                note, penalty, jump = self.note_finder.locate(new_note)
                logging.info(
                    f"New note transcibed: {new_note.name:2}  -->"
                    f" recognized as: {note.name:2}"
                    f" in bar {note.measureNumber:2}"
                    f" beat {float(note.offset+1):4}"
                    f"   {penalty =:6.2f}   {jump=:.2f}"
                )


app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
