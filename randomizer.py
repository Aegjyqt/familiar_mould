from random import choice


class Randomizer:
    """Feeds a random line from a specific list with a reduced chance of the same line repeating two times in a row"""
    _used_phrases = []

    def __init__(self, list_of_elements: list):
        self.list_of_elements = list_of_elements

    def randomize(self, phrases: list) -> str:  # может, отослать к self.list_of_elements?
        if phrases:
            unused_phrases = list(set(phrases) - set(self._used_phrases))
            if unused_phrases:
                chosen_phrase = choice(unused_phrases)
                self._used_phrases.append(chosen_phrase)
                return chosen_phrase
            else:
                self._used_phrases.clear()
                self.randomize(phrases)
        else:
            return "No phrases given"


wise_list = [
    '\'Enough\' is truly powerful a word when you say it to yourself',
    '\'Too much\' is bad. Even if that\'s said about good things',
    'In your case: do more, think less about HOW to do it',
    'Deceit. Self-deceit. Miscommunication. These are the roots of many evils',
    'Do not despair. Do not presume.',
    'Do what you must, and come what may',
    'Now that you don\'t have to be perfect, you can be good.'
]
