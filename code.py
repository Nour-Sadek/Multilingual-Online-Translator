# Imported packages
import requests
from bs4 import BeautifulSoup

# Constants
ORIGINAL_URL = 'https://context.reverso.net/translation/'
LANGUAGE_LOOKUP = {'fr': 'french', 'en': 'english'}
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# Read user input
while True:
    print('Type "en" if you want to translate from French into English, or \
"fr" if you want to translate from English into French:')
    lang_to = input()
    if lang_to == 'fr':
        lang_from = 'en'
        break
    elif lang_to == 'en':
        lang_from = 'fr'
        break
    else:
        print('Incorrect Format')

# Take the word to be translated from the user
print('Type the word you want to translate:')
word_to_translate = input()

print(f'You chose {lang_to} as the language to translate {word_to_translate}.')

# Create teh website url from which the translation will be extracted
website_url = ORIGINAL_URL + \
              f'{LANGUAGE_LOOKUP[lang_from]}-\
{LANGUAGE_LOOKUP[lang_to]}/{word_to_translate}'

# Get the request from the website and extract its content
response = requests.get(website_url, headers=HEADERS)
soup = BeautifulSoup(response.content, 'html.parser')

if response:
    print(response.status_code, 'OK', end='\n\n')

# Getting the translations to the required word
word_translations = soup.find_all('span', {'class': 'display-term'})
word_translations = [word.text for word in word_translations]

# Printing only the first 5 provided translations
print(f'{LANGUAGE_LOOKUP[lang_to].title()} Translations:')
for word in word_translations[:5]:
    print(word)
print()

# Getting the examples
examples = soup.find_all('div', {'class': ['src', 'trg']})
examples = [example.text.strip() for example in examples]
examples = [example for example in examples if example != '']

# Separating the examples according to the language
lang_from_examples = examples[::2]
lang_to_examples = examples[1::2]

# Printing only the first 5 provided examples
print(f'{LANGUAGE_LOOKUP[lang_to].title()} Examples:')
for i in range(5):
    print(lang_from_examples[i] + '\n' + lang_to_examples[i] + '\n')
