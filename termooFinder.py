import csv
import colorama
from pathlib import Path
from operator import itemgetter

colorama.init()
GREEN = colorama.Fore.GREEN
YELLOW = colorama.Fore.YELLOW
RED = colorama.Fore.RED
CYAN = colorama.Fore.CYAN


def find_words(data_path: Path):
    """
    Creates new csv file that only contains 5 letter words, with the same fildnames set in data.csv

    :param data_path: path to the csv file that contains words in pt_br (data.csv)

    """
    output_path = Path.cwd() / 'termoos'
    with open(data_path, "r", encoding='utf-8') as data:
        words = csv.DictReader(data)
        fieldnames = words.fieldnames
        with open((output_path / 'data_five.csv'), 'a', encoding='utf-8', newline='') as output_writer:
            count = 0
            output = csv.DictWriter(output_writer, fieldnames=fieldnames)
            output.writeheader()
            for word in words:
                if len(word['name']) == 5:
                    count = count + 1
                    print(f'{CYAN}[*]Found {count} words...')
                    output.writerow(word)


def get_five_letter_words():
    """
    Runs the find_words() method. find_words() needs to execute just one time. This is for organization purposes.
    """
    print(f'{GREEN}[✓]Starting process...\n')
    data_path = (Path.cwd() / 'termoos' / 'data.csv')
    find_words(data_path)
    print(f'\n{GREEN}[✓]Finished')


def get_possible_words(wrong_letters: list):
    """
    Get all the words that contains the characters specified in the 'letters' list
    :param wrong_letters: list with the
    :return:
    """
    if len(wrong_letters) == 0:
        print(f'{RED}[!]Words needs letters pal...')
        return

    possible_words = []
    data_five_path = Path.cwd() / 'termoos' / 'data_five.csv'
    with open(data_five_path, 'r', encoding='utf-8') as data_five:
        words = csv.DictReader(data_five)
        for word in words:
            result = [letter not in word['name'] for letter in wrong_letters]
            # print(result)
            if all(result):
                possible_words.append(word)

    possible_words = get_best_prob_order(possible_words)
    possible_words = get_only_words(possible_words)
    return possible_words


def possible_by_rigth_letters(words: list, correct_letters: list):
    possible_words = []
    for word in words:
        result = [letter in word for letter in correct_letters]
        # print(result)
        if all(result):
            possible_words.append(word)
    return possible_words


def possible_by_wrong_letters(words: list, wrong_letters: list):
    possible_words = []
    for word in words:
        result = [letter not in word for letter in wrong_letters]
        # print(result)
        if all(result):
            possible_words.append(word)
    return possible_words


def tf_to_int(words: list):
    """
    Convert the 'tf' values from string to int

    :param words: list of dict that contains the words and info
    :return: list of dict with the 'tf' value converted

    """
    for word in words:
        word['tf'] = int(word['tf'])
    return words


def get_best_prob_order(possible_words: list):
    """
    Sort the possible words by the 'tf' key in descending order

    :param possible_words: list of dict that contains all the possible correct words
    :return: return the same list but sorted
    """
    possible_words = tf_to_int(possible_words)
    possible_words = sorted(possible_words, key=itemgetter('tf'), reverse=True)
    return possible_words


def get_only_words(words_dict_list: list):
    """
    Get only the 'name' value from the words list of dicts

    :param words_dict_list: list of dicts that contains the words
    :return: list of string containig the words
    """
    only_words = []
    for word in words_dict_list:
        only_words.append(word["name"])
    return only_words


def wrong_place(possible_words: list, letter_wrong_placement: list):
    new_possible_words = possible_words
    for word in possible_words:
        for letter in letter_wrong_placement:
            if word.startswith(letter["letter"], letter["index"]):
                new_possible_words.remove(word)
                break
    return new_possible_words


def right_place(possible_words: list, letter_right_placement: list):
    new_possible_words = []
    for word in possible_words:
        for letter in letter_right_placement:
            if word.startswith(letter["letter"], letter["index"]):
                new_possible_words.append(word)
                break
    return new_possible_words


def main():
    wrong_letters = ['u', 'd', 'i', 'o', 't', 's']
    right_letter = ['a', 'n', 'e']

    letter_wrong_placement = [{'letter': 'n', 'index': 1}, {'letter': 'e', 'index': 3}]
    letter_right_placement = [{'letter': 'a', 'index': 0}]

    possible_words = get_possible_words(wrong_letters)
    possible_words = possible_by_rigth_letters(possible_words, right_letter)

    possible_words = wrong_place(possible_words, letter_wrong_placement)
    possible_words = right_place(possible_words, letter_right_placement)

    print(f'Possible TERMOOS: {len(possible_words)}')
    for word in possible_words:
        print(f'{GREEN} {word}')


if __name__ == '__main__':
    main()
