#!/usr/bin/python

# Copyright (c) 2011 British Broadcasting Corporation
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
from ConfigParser import ConfigParser
import os, sys, re
import json
from transcriber import Transcriber

def main():
    parser = argparse.ArgumentParser(description='Evaluate Sphinx3 WER on speech/transcripts dataset')
    parser.add_argument('--config', metavar='INI', type=str, default='sphinx-config.ini', help='A configuration file specifying which models to use (default: %(default)s)')
    parser.add_argument('--directory', metavar='DIR', type=str, default='reith-lectures', help='Path to the evaluation dataset (default: %(default)s)')
    parser.add_argument('--lazy', metavar='L', type=bool, default=False, help='If set to true, do not attempt to derive any new data (default: %(default)s)')
    args = parser.parse_args()
    lazy = args.lazy
    directory = args.directory
    config = ConfigParser()
    config_models = args.config
    transcriber = Transcriber()
    if not lazy:
        config.readfp(open(config_models))
        config.items('models')
        acoustic_model = config.get('models', 'acoustic_model')
        dictionary = config.get('models', 'dictionary')
        filler = config.get('models', 'filler')
        language_model = config.get('models', 'language_model')
        convert_pdf_to_text(directory)
        transcriber.initialise(acoustic_model, dictionary, filler, language_model)
    evaluate(transcriber, directory, lazy)

def convert_pdf_to_text(directory):
    print >> sys.stderr, "Converting all PDFs under %s to text" % directory
    for file_name in os.listdir(directory):
        if file_name.endswith('.pdf'):
            print >> sys.stderr, "Converting %s to text" % file_name
            os.system('pdftotext "' + os.path.join(directory, file_name) + '"')

def extract_transcript_from_text(text_file):
    data = open(text_file).read().decode('utf8')
    data = ' '.join(re.split(r'\n[1-9]+\n', data)) # getting rid of page numbers
    data_s = data.split('RADIO 4')
    if len(data_s) > 1:
        data_s = data_s[1]
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

def word_error_rate(t1, t2):
    a = t1.split(' ')
    b = t2.split(' ')
    n = len(a)
    m = len(b)
    if n > m:
        a,b = b,a
        n,m = m,n
    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)
    return (current[n] / float(m))

def evaluate(transcriber, directory, lazy):
    wers = []
    for file_name in os.listdir(directory):
        if not lazy and file_name.endswith('.mp3') and not os.path.exists(os.path.join(directory, file_name.split('.mp3')[0] + '.sphinx.txt')):
            raw_file = '/tmp/sphinx-eval.raw'
            print >> sys.stderr, "Transcribing %s" % file_name
            os.system('sox "' + os.path.join(directory, file_name) + '" -r 14000 -c 1 -s ' + raw_file)
            (sphinx_transcript, details) = transcriber.transcribe(raw_file)
            sphinx_transcript_f = open(os.path.join(directory, file_name.split('.mp3')[0] + '.sphinx.txt'), 'w')
            sphinx_transcript_f.write(sphinx_transcript)
            sphinx_transcript_f.close()
            details_f = open(os.path.join(directory, file_name.split('.mp3')[0] + '.sphinx.json'), 'w')
            details_f.write(json.dumps(details))
            details_f.close()
    for file_name in os.listdir(directory):
        if file_name.endswith('.sphinx.txt'):
            sphinx_transcript = open(os.path.join(directory, file_name)).read()
            transcript = extract_transcript_from_text(os.path.join(directory, file_name.split('.sphinx.txt')[0] + '.txt'))
            wer = word_error_rate(sphinx_transcript, transcript)
            print "WER for %s: %f" % (file_name, wer)
            wers += [ wer ]
    print "Average WER: %f" % (sum(wers, 0.0) / len(wers),)

main()
