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


class WebsiteNotFoundError(Exception):
    pass


# Helper Functions
def check_orig_lang() -> str:
    """Return user input for the original langauge from which they want to
    translate a word from."""

    while True:
        print('Type the number of your language:')
        lang_from = input()
        if lang_from not in LANGUAGE_LOOKUP:
            print('Incorrect input.')
        else:
            return lang_from


def check_lang_to(lang_from: str) -> str:
    """Return user input for the language(s) they want to translate to."""

    while True:
        print("Type the number of a language you want to translate to or '0' \
to translate to all languages:")
        lang_to = input()
        if lang_to == '0':
            return lang_to
        elif lang_to not in LANGUAGE_LOOKUP:
            print('Incorrect input.')
        elif lang_to == lang_from:
            print('This should be different from the original language.')
        else:
            return lang_to


def get_translations(lang_from: str, lang_to: [str], word_to_translate: str) -> str:
    """Return a formatted string representing the translation of
    <word_to_translate> from <lang_from> to every language in the list
    <lang_to>.

    Raise WebsiteNotFoundError if the provided <word_to_translate> is not
    found in the Context Reverso website.
    """

    translations = ''
    for lang in lang_to:
        # Create the website url from which the translation will be extracted
        website_url = ORIGINAL_URL + f'{lang_from}-{lang}/{word_to_translate}'

        # Get the request from the website and check if website exists
        response = requests.get(website_url, headers=HEADERS)
        if str(response.status_code).startswith('4'):
            raise WebsiteNotFoundError(f"Sorry, couldn't find the word \
{word_to_translate}")

        # Extract the contents from the url
        soup = BeautifulSoup(response.content, 'html.parser')

        # Getting the translations to the required word
        word_translations = soup.find_all('span', {'class': 'display-term'})
        word_translations = [word.text for word in word_translations]

        # Storing only the first 5 provided translations
        translations = translations + f'{lang.title()} Translations:\n'
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

        # Storing only the first 5 provided examples
        translations = translations + f'{lang.title()} Examples:\n'
        for i in range(5):
            translations = translations + lang_from_examples[i] + '\n' + \
                           lang_to_examples[i] + '\n\n'

    return translations


# Printing the welcoming message showcasing the languages this translator can
# support
print('Hello, welcome to the translator. Translator supports:')
for key, value in LANGUAGE_LOOKUP.items():
    print(f'{key}. {value.title()}')

# Take the language the user wants to translate from
lang_from = check_orig_lang()

# Take the language the user wants to translate to
lang_to = check_lang_to(lang_from)

# Take the word the iser wishes to translate
print('Type the word you want to translate:')
word_to_translate = input().lower()
print()

lang_from = LANGUAGE_LOOKUP[lang_from]

# Get the list of language(s) the user wants to translate <word_to_translate>
# to
if lang_to != '0':
    lang_to = [LANGUAGE_LOOKUP[lang_to]]
else:
    lang_to = [lang for lang in list(LANGUAGE_LOOKUP.values()) if lang != lang_from]

# Save the translations according to user requirements
translations = get_translations(lang_from, lang_to, word_to_translate)

# Save the output of the translations to a file under the name
# <word_to_translate.txt>
file = open(f'{word_to_translate}.txt', 'w')
file.write(translations)
file.close()

print(translations)
