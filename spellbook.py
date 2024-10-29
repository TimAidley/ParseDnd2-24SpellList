from bs4 import BeautifulSoup
from spell import Spell

class SpellBook:
    def __init__(self, source):
        self.spells = []
        if source[:4] == "http":
            # load from url
            pass
        elif source[-5:] == ".html":
            # load from a stored file
            with open(source, "rt", errors='replace', encoding='utf8') as file:
                html_doc = file.read()
                self.interpret_html_as_spells(html_doc)
        else:
            # treat source as raw html
            pass

    def interpret_html_as_spells(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        spell_section = soup.find('div', class_="p-article-content u-typography-format")
        for section in spell_section.find_all('h3'):
            spell = Spell(section)
            self.spells.append(spell)

    def print_summary_of_spells(self):
        print(f"{len(self.spells)} spells in total.")
        classes = set()
        for spell in self.spells:
            for c in spell.classes:
                classes.add(c)

        for c in classes:
            class_spells = sorted(filter(lambda x: c in x.classes, self.spells), key=lambda x: x.level)
            print(f"{c}: {len(class_spells)} spells")



if __name__ == "__main__":
    spellbook = SpellBook("Spell Descriptions - Player’s Handbook - Dungeons & Dragons - Sources - D&D Beyond.html")
    spellbook.print_summary_of_spells()
