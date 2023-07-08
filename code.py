# Imported packages
import requests
from bs4 import BeautifulSoup

# Constants
ORIGINAL_URL = 'https://context.reverso.net/translation/'
LANGUAGE_LOOKUP = {'1': 'arabic',
                   '2': 'german',
                   '3': 'english',
                   '4': 'spanish',
                   '5': 'french',
                   '6': 'hebrew',
                   '7': 'japanese',
                   '8': 'dutch',
                   '9': 'polish',
                   '10': 'portuguese',
                   '11': 'romanian',
                   '12': 'russian',
                   '13': 'turkish'}
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# Printing the welcoming message showcasing the languages this translator can
# support
print('Hello, welcome to the translator. Translator supports:')
for key, value in LANGUAGE_LOOKUP.items():
    print(f'{key}. {value.title()}')

# Take the language the user wants to translate from
while True:
    print('Type the number of your language:')
    lang_from = input()
    if lang_from not in LANGUAGE_LOOKUP:
        print('Incorrect input.')
    else:
        break

# Take the language the user wants to translate to
while True:
    print("Type the number of a language you want to translate to or '0' to \
translate to all languages:")
    lang_to = input()
    if lang_to == '0':
        break
    elif lang_to not in LANGUAGE_LOOKUP:
        print('Incorrect input.')
    elif lang_to == lang_from:
        print('This should be different from the original language.')
    else:
        break

print('Type the word you want to translate:')
word_to_translate = input().lower()
print()

translations = ''
if lang_to != '0':
    # Create the website url from which the translation will be extracted
    website_url = ORIGINAL_URL + \
                  f'{LANGUAGE_LOOKUP[lang_from]}-\
{LANGUAGE_LOOKUP[lang_to]}/{word_to_translate}'

    # Get the request from the website and extract its content
    response = requests.get(website_url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Getting the translations to the required word
    word_translations = soup.find_all('span', {'class': 'display-term'})
    word_translations = [word.text for word in word_translations]

    # Printing only the first 5 provided translations
    translations = translations + f'{LANGUAGE_LOOKUP[lang_to].title()} \
Translations:\n'
    for word in word_translations[:5]:
        translations = translations + word + '\n'
    translations = translations + '\n'

    # Getting the examples
    examples = soup.find_all('div', {'class': ['src', 'trg']})
    examples = [example.text.strip() for example in examples]
    examples = [example for example in examples if example != '']

    # Separating the examples according to the language
    lang_from_examples = examples[::2]
    lang_to_examples = examples[1::2]

    # Printing only the first 5 provided examples
    translations = translations + f'{LANGUAGE_LOOKUP[lang_to].title()} \
Examples:\n'
    for i in range(5):
        translations = translations + lang_from_examples[i] + '\n' + \
                       lang_to_examples[i] + '\n\n'
else:
    for key, value in LANGUAGE_LOOKUP.items():
        if key == lang_from:
            pass
        else:
            website_url = ORIGINAL_URL + \
                          f'{LANGUAGE_LOOKUP[lang_from]}-\
{value}/{word_to_translate}'

            response = requests.get(website_url, headers=HEADERS)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Getting the translations to the required word
            word_translations = soup.find_all('span', {'class': 'display-term'})
            word_translations = [word.text for word in word_translations]

            # Printing only the first provided translations
            translations = translations + f'{value.title()} Translations:\n'
            translations = translations + word_translations[0] + '\n\n'

            # Getting the examples
            examples = soup.find_all('div', {'class': ['src', 'trg']})
            examples = [example.text.strip() for example in examples]
            examples = [example for example in examples if example != '']

            # Separating the examples according to the language
            lang_from_examples = examples[::2]
            lang_to_examples = examples[1::2]

            # Printing only the first provided examples
            translations = translations + f'{value.title()} Examples:\n'
            translations = translations + lang_from_examples[0] + '\n' + \
                lang_to_examples[0] + '\n\n'

# Save the output of the translations to a file under the name
# <word_to_translate.txt>
file = open(f'{word_to_translate}.txt', 'w')
file.write(translations)
file.close()

print(translations)
