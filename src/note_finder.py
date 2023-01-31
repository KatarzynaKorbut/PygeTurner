from collections import deque
from typing import Deque, Iterable, List, Tuple

from fuzzysearch import Match, find_near_matches
from music21.note import Note
from music21.stream.iterator import StreamIterator


class NoteFinder:
    MIN_NOTE_HISTORY = 3
    MAX_NOTE_HISTORY = 6

    @staticmethod
    def notes_to_pitch_classes(notes: Iterable[Note]) -> List[int]:
        return [note.pitch.pitchClass for note in notes]

    def __init__(self, sheet_notes: StreamIterator[Note]):
        self.sheet_notes = sheet_notes
        self.sheet_note_pitch_classes = self.notes_to_pitch_classes(self.sheet_notes)
        self.next_offset = 0
        self.note_history: Deque[Note] = deque(maxlen=self.MAX_NOTE_HISTORY)

    @classmethod
    def notes_match(cls, note_a: Note, note_b: Note):
        return note_a.pitch.pitchClass == note_b.pitch.pitchClass

    def jump_distance(self, match: Match) -> float:
        match_last_note = self.sheet_notes[match.end - 1]
        match_last_note_position = match_last_note.getOffsetInHierarchy(
            self.sheet_notes.srcStream
        )
        next_note = self.sheet_notes[self.next_offset]
        next_note_position = next_note.getOffsetInHierarchy(self.sheet_notes.srcStream)

        beat_distance = float(match_last_note_position - next_note_position)
        return abs(beat_distance)

    def match_penalty(self, match: Match) -> float:
        JUMP_FACTOR = 1 / 5
        return match.dist + self.jump_distance(match) * JUMP_FACTOR

    def locate(self, new_note: Note) -> Tuple[Note, float, float]:
        self.note_history.append(new_note)

        self.next_offset = min(self.next_offset, len(self.sheet_note_pitch_classes) - 1)
        next_note = self.sheet_notes[self.next_offset]
        if len(self.note_history) < self.MIN_NOTE_HISTORY:
            self.next_offset += 1
            return next_note, -1, 0
        else:
            note_history_pitch_classes = self.notes_to_pitch_classes(self.note_history)
            matches = list(
                find_near_matches(
                    note_history_pitch_classes,
                    self.sheet_note_pitch_classes,
                    max_l_dist=len(note_history_pitch_classes) // 3,
                )
            )
            if len(matches) == 0:
                self.next_offset += 1
                return next_note, -1, 0

            best_match = min(matches, key=lambda m: self.match_penalty(m))
            penalty = self.match_penalty(best_match)
            jump = self.jump_distance(best_match)

            self.next_offset = best_match.end
            next_note = self.sheet_notes[self.next_offset - 1]

            return next_note, penalty, jump
