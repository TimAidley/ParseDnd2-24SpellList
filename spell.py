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

with open("Spell Descriptions - Player’s Handbook - Dungeons & Dragons - Sources - D&D Beyond.html", "rt", errors='replace', encoding='utf8') as file:
    html_doc = file.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    spell_section = soup.find('div', class_="p-article-content u-typography-format")
    spells = []
    for section in spell_section.find_all('h3'):
        spell = Spell(section)
        spells.append(spell)

    print (f"{len(spells)} spells in total.")

    classes = set()
    for spell in spells:
        for c in spell.classes:
            classes.add(c)

    for c in classes:

        class_spells = sorted(filter(lambda x : c in x.classes, spells), key=lambda x : x.level)
        print(f"{c}: {len(class_spells)} spells")

        #for spell in bard_spells:
        #    if spell.level == 0:
        #        print(f'{spell.name}: {spell.type} Cantrip')
        #    else:
        #        print(f'{spell.name}: Level {spell.level} {spell.type}')





