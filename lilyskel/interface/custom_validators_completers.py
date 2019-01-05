from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.validation import Validator, ValidationError

from lilyskel import info, mutopia
from lilyskel.interface import common
from lilyskel.lynames import VALID_CLEFS


class InsensitiveCompleter(Completer):
    """Complete without caring about case."""

    def __init__(self, word_list):
        self._word_list = set(word_list)

    def get_completions(self, document, complete_event):
        start = - len(document.text)
        for word in self._word_list:
            if document.text.lower() in word.lower():
                yield Completion(word, start_position=start)


class YNValidator(Validator):
    """Validates Yes/No responses in prompt_toolkit"""

    def validate(self, document):
        text = document.text
        if not text:
            raise ValidationError(message="Response Required", cursor_position=0)
        if text.lower()[0] not in 'yn':
            raise ValidationError(message="Response must be [y]es or [n]o",
                                  cursor_position=0)


class IndexValidator(Validator):
    """Validates indexes of lists."""

    def __init__(self, max_len, allow_empty=True):
        self.max = max_len
        self.allow_empty = allow_empty

    def validate(self, document):
        text = document.text
        if not text and self.allow_empty:
            return
        try:
            idx = int(text)
        except ValueError:
            raise ValidationError(message="Input must be number",
                                  cursor_position=0)
        if idx > self.max:
            raise ValidationError(message="Index out of range",
                                  cursor_position=0)


class LanguageValidator(Validator):
    def validate(self, document):
        if not document.text:
            raise ValidationError(message="Response Required", cursor_position=0)
        if document.text not in info.get_valid_languages():
            raise ValidationError(message="Invalid language", cursor_position=0)


class LicenseValidator(Validator):
    def validate(self, document):
        if not document.text:
            raise ValidationError(message="Response Required", cursor_position=0)
        if document.text not in mutopia.get_licenses():
            raise ValidationError(message="Invalid license", cursor_position=0)


class StyleValidator(Validator):
    def validate(self, document):
        if not document.text:
            raise ValidationError(message="Response Required", cursor_position=0)
        if document.text not in mutopia.get_styles():
            raise ValidationError(message="Invalid style", cursor_position=0)


class ModeValidator(Validator):
    def validate(self, document):
        if not document.text:
            raise ValidationError(message="Response Required", cursor_position=0)
        if document.text not in info.get_allowed_modes():
            raise ValidationError(message="Invalid mode", cursor_position=0)


class NoteValidator(Validator):
    def validate(self, document):
        if not document.text:
            raise ValidationError(message="Response Required", cursor_position=0)
        if document.text not in info.get_allowed_notes():
            raise ValidationError(message="Invalid note", cursor_position=0)


class IsNumberValidator(Validator):
    def validate(self, document, allow_empty=True):
        text = document.text
        if not text and allow_empty:
            return
        if not text.isdigit():
            raise ValidationError(message="Must be integer")
        try:
            int(text)
        except ValueError as err:
            raise ValidationError(message=err)


class ClefValidator(Validator):
    def validate(self, document):
        if not document.text:
            return
        if document.text not in VALID_CLEFS:
            raise ValidationError(message="Invalid clef", cursor_position=0)
