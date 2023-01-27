import logging
from collections import deque
from typing import Deque, Iterable, Sequence

from fuzzysearch import Match, find_near_matches
from music21.note import Note


class NoteFinder:
    def __init__(self, sheet_notes: Sequence[Note]):
        self.sheet_notes = sheet_notes
        self.next_offset = 0
        self.note_history: Deque[Note] = deque(maxlen=5)

    @classmethod
    def matches(cls, note_a: Note, note_b: Note):
        return note_a.name == note_b.name

    def jump_distance(self, match: Match):
        return abs(match.end - self.next_offset)

    @staticmethod
    def note_names(note_list: Iterable[Note]):
        return [n.name for n in note_list]

    def locate(self, new_note: Note) -> Note:
        self.note_history.append(new_note)

        next_note = self.sheet_notes[self.next_offset]
        if self.matches(new_note, next_note):
            self.next_offset += 1
            return next_note
        else:
            note_history = list(self.note_history)
            matches = find_near_matches(
                self.note_names(note_history),
                self.note_names(self.sheet_notes),
                max_l_dist=len(note_history) - 1)
            matches = sorted(matches, key=lambda m: (m.dist, self.jump_distance(m)))
            best_match = matches[0]
            logging.debug("NoteFinder best match: %s", best_match)
            self.next_offset = best_match.end
            next_note = self.sheet_notes[best_match.end - 1]
            return next_note
