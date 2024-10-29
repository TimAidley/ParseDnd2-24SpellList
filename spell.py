from bs4 import BeautifulSoup

class Spell:
    def __init__(self, spell):
        self.name = spell.text


        # Parse the meta data
        meta = spell.find_next('p')
        (type_level, classes) = meta.text.split('(')
        type_level_words = type_level.strip().split(' ')
        if type_level_words[0] == 'Level':
            self.level = int(type_level_words[1])
            self.type = type_level_words[2]
        elif type_level_words[1] == 'Cantrip':
            self.level = 0
            self.type = type_level_words[0]
        else:
            raise NameError(f"'{type_level}' not understood while parsing '{self.name}'.")
        self.classes = classes[:-1].split(', ')

        # Parse the spell attributes
        info = meta.find_next('div')
        for attr in info.children:
            if attr.name == 'p':
                key = attr.contents[0].text
                value = attr.contents[1].text
                match key:
                    case 'Casting Time:':
                        self.cast_time = value
                    case 'Range:':
                        self.range = value
                    case 'Components:':
                        self.components = value
                    case 'Component:':
                        self.components = value
                    case 'Duration:':
                        self.duration = value
                    case _:
                        raise NameError(f"{key} is an unknown attribute in '{self.name}'.")

        # Read the description.
        # Todo: Convert the emphasised text to markdown?
        desc = info.next_sibling.find_next('p')
        self.description = []
        while desc.name == 'p':
            self.description += desc.text
            desc = desc.find_next(['p', 'hr', 'div'])

    def __str__(self):
        return f"'{self.name}': Level {self.level} {self.type} ({' '.join(self.classes)})"

