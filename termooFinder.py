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


def tf_to_int(words: list):
    for word in words:
        word['tf'] = int(word['tf'])
    return words


def get_five_letter_words():
    print(f'{GREEN}[✓]Starting process...\n')
    data_path = (Path.cwd() / 'termoos' / 'data.csv')
    find_words(data_path)
    print(f'\n{GREEN}[✓]Finished')


def get_possible_words(letters: list):
    if len(letters) > 5:
        print(f'{RED}[!]Words cannot have more than 5 letters')
        return
    if len(letters) == 0:
        print(f'{RED}[!]Words needs letters pal...')
        return
    possible_words = []
    data_five_path = Path.cwd() / 'termoos' / 'data_five.csv'
    with open(data_five_path, 'r', encoding='utf-8') as data_five:
        words = csv.DictReader(data_five)
        for word in words:
            result = [letter in word['name'] for letter in letters]
            # print(result)
            if all(result):
                possible_words.append(word)
    return possible_words


def get_best_prob_order(possible_words: list):
    possible_words = tf_to_int(possible_words)
    sorted_words = sorted(possible_words, key=itemgetter('tf'), reverse=True)
    return sorted_words


def main():
    letters = ['r']
    words = get_possible_words(letters)
    # for word in words:
    #     print(f'{RED}UNORDERED: {word}')

    result = get_best_prob_order(words)
    for word in result:
        print(f'{GREEN}SORTED: {word}')


if __name__ == '__main__':
    main()
