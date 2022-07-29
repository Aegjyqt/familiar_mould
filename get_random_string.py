from random import randint

class Randomizer:
    """Feeds a random line from a specific list with a reduced chance of the same line repeating two times in a row"""
    copy = []

    def __init__(self, list: list) -> str:
        self.list = list

    def get_random(self):
        while True:
            output = self.list[randint(0, len(self.list) - 1)]
            if output not in self.copy:
                self.copy.append(output)
                return output
            elif output in self.copy and len(self.copy) != len(self.list):
                continue
            else:
                self.copy = []

wise_list = ['\'Enough\' is truly powerful a word when you say it to yourself',
                 '\'Too much\' is bad. Even if that\'s said about good things',
                 'In your case: do more, think less about HOW to do it',
                 'Deceit. Self-deceit. Miscommunication. These are the roots of many evils',
                 'Do not despair. Do not presume.',
                 'Do what you must, and come what may']