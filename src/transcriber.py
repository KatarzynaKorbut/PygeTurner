import logging
from typing import cast

import librosa
import numpy
from music21.note import Note


class Transcriber:
    def __init__(self):
        self.n_bins: int
        self.set_note_range("A0", "C8")  # zakres fortepianu

    def load(self, file_path):
        self.samples, self.sampling_rate = librosa.load(file_path)
        logging.info("Częstotliwość próbkowania: %d", self.sampling_rate)
        logging.info("Całkowita liczba próbek: %d", self.samples.shape)
        logging.info("Czas trwania: %.1f s", self.samples.shape[0] / self.sampling_rate)

        self.f0 = self.base_frequency(
            self.samples, self.sampling_rate, self.note_lowest_hz, self.note_highest_hz
        )
        onset_frames = self.onset_frames(self.samples, self.sampling_rate)
        self.notes_with_times = self.get_notes_with_times(
            self.f0, self.sampling_rate, onset_frames
        )

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
        return librosa.onset.onset_detect(y=samples, sr=sampling_rate, units="frames")

    @staticmethod
    def get_notes_with_times(f0, sampling_rate, onset_frames):
        onset_times = librosa.frames_to_time(onset_frames, sr=sampling_rate)
        note_durations = numpy.diff(onset_times)

        note_fragments = numpy.split(f0, onset_frames)[1:]

        max_percent_of_nans = 0.5
        valid_fragments = [
            numpy.count_nonzero(numpy.isnan(fragment))
            < len(fragment) * max_percent_of_nans
            for fragment in note_fragments
        ]

        note_frequencies = [numpy.nanmedian(fragment) for fragment in note_fragments]
        pitch_spaces = librosa.hz_to_midi(note_frequencies)
        notes = [
            (Note(ps), onset_time)
            for is_valid, ps, onset_time in zip(
                valid_fragments, pitch_spaces, onset_times
            )
            if is_valid
        ]
        return notes

    def set_note_range(self, note_lowest, note_highest):
        self.note_lowest_hz = librosa.note_to_hz(note_lowest)
        self.note_highest_hz = librosa.note_to_hz(note_highest)

        note_lowest_midi = cast(int, librosa.note_to_midi(note_lowest))
        note_highest_midi = cast(int, librosa.note_to_midi(note_highest))
        self.n_bins = (
            note_highest_midi - note_lowest_midi + 1
        )  # Number of frequency bins

        logging.info(
            "Note range: lowest = %s (%.2f Hz), highest = %s (%.2f Hz), n_bins=%d",
            note_lowest,
            self.note_lowest_hz,
            note_highest,
            self.note_highest_hz,
            self.n_bins,
        )
