#!/usr/bin/python

import argparse
from ConfigParser import ConfigParser
import os, sys, re
from transcriber import Transcriber

def main():
    parser = argparse.ArgumentParser(description='Evaluate Sphinx3 WER on speech/transcripts dataset')
    parser.add_argument('models', metavar='configuration file', type=str, nargs=1, help='A configuration file specifying which models to use')
    parser.add_argument('--directory', metavar='dataset directory', type=str, nargs=1, help='Path to the evaluation dataset')
    args = parser.parse_args()
    convert_pdf_to_text(args.directory)
    config = ConfigParser()
    config.readfp(open(args.models))
    config.items('models')
    acoustic_model = config.get('models', 'acoustic_model')
    dictionary = config.get('models', 'dictionary')
    filler = config.get('models', 'filler')
    language_model = config.get('models', 'language_model')
    transcriber = Transcriber()
    transcriber.initialise(acoustic_model, dictionary, filler, language_model)

def convert_pdf_to_text(directory):
    for file_name in os.listdir(directory):
        if file_name.endswith('.pdf'):
            print >> sys.stderr, "Converting %s to text", [ file_name ]
            os.system('pdftotext ' + file_name)

def extract_transcript_from_text(text_file):
    data = open(text_file).read().decode('utf8')
    data = ' '.join(re.split(r'\n[1-9]+\n', data)) # getting rid of page numbers
    data = data.split('RADIO 4')[1]
    transcript = ''
    for item in re.split(r'\n[A-Z ]+:', data):
        item = re.sub('\n', ' ', item)
        item = re.sub(u'\u2019', '\'', item)
        item = re.sub('\(APPLAUSE\)', ' ', item)
        item = re.sub('\(LAUGHTER\)', ' ', item)
        item = re.sub(r'[^a-zA-Z0-9 ]', '', item).lower()
        transcript += ' ' + item
    transcript = re.sub(r'( )+', ' ', transcript)
    return transcript


main()
