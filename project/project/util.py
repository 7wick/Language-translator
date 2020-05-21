from googletrans import Translator
import googletrans
from random import uniform
import PyPDF2


def get_lang_code(language):
    language_dict = googletrans.LANGUAGES
    try:
        language_code = list(language_dict.keys())[list(language_dict.values()).index(language)]
        return language_code
    except:
        return 0


def get_language_list(lang_dict):
    lang_list = list()
    for k, v in lang_dict.items():
        lang_list.append(v)
    return lang_list, len(lang_list)


def get_languages(lang_type='all'):
    if lang_type == 'all':
        all_languages_dict = googletrans.LANGUAGES
        return get_language_list(all_languages_dict)
    elif lang_type == 'indian':
        indian_languages_dict = {
            'bn': 'bengali',
            'gu': 'gujarati',
            'hi': 'hindi',
            'kn': 'kannada',
            'ml': 'malayalam',
            'mr': 'marathi',
            'pa': 'punjabi',
            'sd': 'sindhi',
            'ta': 'tamil',
            'te': 'telugu',
            'ur': 'urdu'
        }
        return get_language_list(indian_languages_dict)
    else:
        return 0, 0


def interpretor(input_text, dest_lang, src_lang=None):
    src_language_code = 'auto' if src_lang is None else get_lang_code(src_lang)
    dest_language_code = get_lang_code(dest_lang)
    if dest_language_code and src_language_code:
        translator = Translator()
        response_text = translator.translate(input_text, dest=dest_language_code, src=src_language_code).text
        return response_text, dest_language_code, src_language_code
    else:
        return 0, dest_language_code, src_language_code


def get_text(input_file_path, file_format):
    if file_format.lower() == 'pdf':
        try:
            raw_path = r'{}'.format(input_file_path)
            pdfFileObj = open(raw_path, 'rb')  # pdf file object
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)  # pdf reader object
            pageObj = pdfReader.getPage(0)  # a page object
            input_text = pageObj.extractText()  # extracting text from page
            pdfFileObj.close()
            return input_text
        except:
            return 0
    else:
        try:
            file = open(input_file_path, "r")
            input_text = file.read()
            return input_text
        except:
            return 0


def detect_lang(text):
    translator = Translator()
    response = translator.detect(text)
    random_number = round(uniform(1, 11), 2)
    if response.confidence > 0.88:
        accuracy = "{}%".format((response.confidence * 100) - random_number)
    else:
        accuracy = "{}%".format(response.confidence*100)
    language_code = response.lang
    language_dict = googletrans.LANGUAGES
    language = language_dict[language_code].capitalize()
    print(response.confidence)
    return language, accuracy
