from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.validation import Validator, ValidationError


def instruments_with_indexes(instrumentlist):
    for idx, instrument in enumerate(instrumentlist):
        print(f"{idx}: {instrument.part_name()}")


class InsensitiveCompleter(Completer):
    def __init__(self, word_list):

        self._word_list = word_list

    def get_completions(self, document, complete_event):
        start = - len(document.text)
        for word in self._word_list:
            if document.text.lower() in word.lower():
                yield Completion(word, start_position=start)


class YNValidator(Validator):
    def validate(self, document):
        text = document.text
        if not text:
            raise ValidationError(message="Respose Required", cursor_position=0)
        if text.lower()[0] not in 'yn':
            raise ValidationError(message="Response must be [y]es or [n]o",
                                  cursor_position=0)