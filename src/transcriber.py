import logging
from typing import Iterable

import librosa
import numpy
from music21.note import Note


class Transcriber:
    def __init__(self):
        self.n_bins: int
        self.set_note_range(21, 108)  # zakres fortepianu
        self.has_new_note = False
        self.last_note_number = -1

    def load(self, file_path):
        self.samples, self.sampling_rate = librosa.load(file_path)
        samples_count = self.samples.shape[0]
        logging.info("Częstotliwość próbkowania: %d", self.sampling_rate)
        logging.info("Całkowita liczba próbek: %d", samples_count)
        logging.info("Czas trwania: %.1f s", samples_count / self.sampling_rate)

        self.f0 = self.base_frequency(
            self.samples, self.sampling_rate, self.note_lowest_hz, self.note_highest_hz
        )
        onset_frames = self.onset_frames(self.samples, self.sampling_rate)
        self.notes_with_times = self.get_notes_with_times(
            self.f0, self.sampling_rate, onset_frames
        )

    def update_time(self, seconds: float):
        note_number = self.last_note_number
        # spróbuj cofnąć się do najnowszej nuty przed zadanym czasem
        while note_number > 0 and self.notes_with_times[note_number][1] >= seconds:
            note_number -= 1
        # spróbuj pójść do przodu do najnowszej nuty przed zadanym czasem
        while (
            note_number + 1 < len(self.notes_with_times)
            and self.notes_with_times[note_number + 1][1] < seconds
        ):
            note_number += 1

        if note_number != self.last_note_number:
            self.last_note_number = note_number
            self.has_new_note = True
        else:
            self.has_new_note = False

    def get_new_note(self) -> Note:
        return self.notes_with_times[self.last_note_number][0]

    def spectrogram_image(self):
        spectrogram = librosa.cqt(
            self.samples,
            sr=self.sampling_rate,
            fmin=self.note_lowest_hz,
            n_bins=self.n_bins,
        )

    @staticmethod
    def base_frequency(samples, sampling_rate, note_lowest_hz, note_highest_hz):
        f0, voiced_flag, voiced_probs = librosa.pyin(
            samples,
            sr=sampling_rate,
            fmin=note_lowest_hz,
            fmax=note_highest_hz,
            fill_na=numpy.nan,
            switch_prob=0.9,
        )
        return f0

    @staticmethod
    def onset_frames(samples, sampling_rate):
        return librosa.onset.onset_detect(
            y=samples, sr=sampling_rate, units="frames", backtrack=True
        )

    @staticmethod
    def get_notes_with_times(f0, sampling_rate, onset_frames):
        onset_times: Iterable[float] = librosa.frames_to_time(
            onset_frames, sr=sampling_rate
        )
        note_durations = numpy.diff(onset_times)

        note_fragments = numpy.split(f0, onset_frames)[1:]

        max_percent_of_nans = 0.5
        valid_fragments = [
            numpy.count_nonzero(numpy.isnan(fragment))
            < len(fragment) * max_percent_of_nans
            for fragment in note_fragments
        ]

        note_frequencies = [numpy.nanmedian(fragment) for fragment in note_fragments]
        pitch_spaces: Iterable[float] = librosa.hz_to_midi(note_frequencies)
        notes = [
            (Note(ps), onset_time)
            for is_valid, ps, onset_time in zip(
                valid_fragments, pitch_spaces, onset_times
            )
            if is_valid
        ]
        return notes

    def set_note_range(self, note_lowest_midi: float, note_highest_midi: float):
        self.note_lowest_hz, self.note_highest_hz = librosa.midi_to_hz(
            [note_lowest_midi, note_highest_midi]
        )
        self.n_bins = int(
            note_highest_midi - note_lowest_midi + 1
        )  # Number of frequency bins

        logging.info(
            "Note range: lowest = %s (%.2f Hz), highest = %s (%.2f Hz)",
            librosa.midi_to_note(note_lowest_midi),
            self.note_lowest_hz,
            librosa.midi_to_note(note_highest_midi),
            self.note_highest_hz,
        )
