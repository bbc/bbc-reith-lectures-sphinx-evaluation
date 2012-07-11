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

import _sphinx3
import os

class Transcriber(object):

    _instance = None
    initialised = False
    sphinx3_dir = '/usr/local/share/sphinx3'

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Transcriber, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def initialise(self, acoustic_model, dictionary, fdict, language_model):
        if not self.initialised:
            _sphinx3.parse_argdict({
                'samprate': '14000',
                'nfft': '1024',
                'hmm': acoustic_model,
                'dict': dictionary,
                'fdict': fdict,
                'lm': language_model,
                'beam': '1e-60',
                'wbeam': '1e-40',
                'ci_pbeam': '1e-8',
                'subvqbeam': '1e-2',
                'maxhmmpf': '2000',
                'maxcdsenpf': '1000',
                'maxwpf': '8',
            })
            _sphinx3.init()
            self.initialised = True

    def transcribe(self, raw_audio_file):
        segment_duration = 120
        segment_length = segment_duration * 14000 * 2
        raw = open(raw_audio_file, 'r')
        n = 1 + len(raw.read()) / segment_length
        raw.close()
        transcript = ''
        details = []
        for i in range(0, n):
            raw = open(raw_audio_file, 'r')
            raw.seek(i * segment_length)
            segment_data = raw.read(segment_length)
            raw.close()
            (transcript_s, details_s) = _sphinx3.decode_raw(segment_data)
            transcript += transcript_s + ' '
            details_with_offsets_s = []
            for (term, start, end, s1, s2) in details_s:
                details_with_offsets_s += [ (term, start / 100.0 + i * segment_duration, end / 100.0 + i * segment_duration, s1, s2) ]
            details += details_with_offsets_s
        return (transcript, details)
