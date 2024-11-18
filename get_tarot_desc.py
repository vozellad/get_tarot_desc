import os
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
import json


file_name = 'cards.txt'


def get_desc_from_web(user_input):
    card_url = get_card_url(user_input)
    driver = webdriver.Firefox()
    url = f'https://labyrinthos.co/blogs/tarot-card-meanings-list/{card_url}-tarot-card-meanings'
    driver.get(url)
    desc = get_desc_from_url(driver)
    driver.close()
    return desc


def get_desc_from_url(driver):
    desc = ''
    for n in range(2, 5):
        xpath = f'/html/body/main/div/article/div[2]/div[2]/div/div[1]/p[{n}]'
        desc += driver.find_element(By.XPATH, xpath).text
        desc += '\n'
    desc = desc.replace('.', '.\n')
    return desc


def get_card_url(user_input):
    words = user_input.upper().split()
    if not words:
        raise ValueError(f"card {user_input} doesn't exist")
    initial = words[0]

    if len(words) > 1:
        final = words[1]
        minor_arcana = {
        '1': 'ace',
        'a': 'ace',
        '2': 'two',
        '3': 'three',
        '4': 'four',
        '5': 'five',
        '6': 'six',
        '7': 'seven',
        '8': 'eight',
        '9': 'nine',
        '10': 'ten',
        'P': 'page',
        'KN': 'knight',
        'K': 'king',
        'Q': 'queen',
    }
        suits = {
        'C': 'cups',
        'P': 'pentacles',
        'S': 'swords',
        'W': 'wands',
    }
        initial = minor_arcana.get(initial)
        final = suits.get(final)
        if not final:
            raise ValueError(f"card {user_input} doesn't exist")
        return f'{initial}-of-{final}-meaning'

    major_arcana = {
        '0': 'the-fool',
        'I': 'the-magician',
        'II': 'the-high-priestess',
        'III': 'the-empress',
        'IV': 'the-emperor',
        'V': 'the-hierophant',
        'VI': 'the-lovers',
        'VII': 'the-chariot',
        'VIII': 'strength',
        'IX': 'the-hermit',
        'X': 'the-wheel-of-fortune',
        'XI': 'justice',
        'XII': 'the-hanged-man',
        'XIII': 'death',
        'XIV': 'temperance',
        'XV': 'the-devil',
        'XVI': 'the-tower',
        'XVII': 'the-star',
        'XVIII': 'the-moon',
        'XIX': 'the-sun',
        'XX': 'judgement',
        'XXI': 'the-world',
    }
    card = major_arcana.get(initial)
    if card:
        return f'{card}-meaning-major-arcana'
    raise ValueError(f"card {user_input} doesn't exist")


def get_desc_from_file(user_input):
    global file_name

    # if file empty or uncreated
    if not os.path.isfile(file_name) or os.stat(file_name).st_size == 0:
        return ''

    with open(file_name, 'r+') as f:
        return json.load(f).get(user_input)


def write_desc_to_file(user_input, desc):
    global file_name

    with open('cards.txt', 'w') as f:
        d = {}
        # if file empty or uncreated
        if os.path.isfile(file_name) and os.stat(file_name).st_size > 0:
            d = json.load(f)
        d[user_input] = desc
        json.dump(d, f)


def main():
    arg = sys.argv[1:]
    arg = ' '.join(arg)
    user_input = arg if arg else input('>> ')
    while user_input not in ['exit', 'quit', 'done', 'q']:
        desc = get_desc_from_file(user_input)
        if not desc:
            desc = get_desc_from_web(user_input)
            write_desc_to_file(user_input, desc)
        print(desc, '\n')
        if arg:
            break
        user_input = input('>> ')


if __name__ == '__main__':
    main()