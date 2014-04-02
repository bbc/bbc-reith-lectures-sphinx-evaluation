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

import pocketsphinx as ps
import os, wave, tempfile
from subprocess import Popen
from multiprocessing import Pool, cpu_count

def decode(acoustic_model, dictionary, language_model, data):
    decoder = ps.Decoder(hmm = acoustic_model, lm = language_model, dict = dictionary)
    decoder.start_utt()
    decoder.process_raw(data)
    decoder.end_utt()
    return decoder.get_hyp()[0]

class Transcriber(object):

    def __init__(self, acoustic_model, dictionary, language_model, workers = None, sample_rate = 16000, bits = 16, segment_duration = 120):
        self.acoustic_model = acoustic_model
        self.dictionary = dictionary
        self.language_model = language_model
        self.sample_rate = sample_rate
        self.segment_duration = segment_duration
        self.bits = bits
        if workers is None:
            workers = cpu_count()
        self.pool = Pool(processes = workers)

    def transcribe(self, audio_file):
        wave_file = self.convert(audio_file)
        segment_length = self.segment_duration * self.sample_rate
        wav = wave.open(wave_file)
        nframes = wav.getnframes()
        offset = 0
        results = []
        while offset < nframes:
            audio = wav.readframes(segment_length)
            result = self.pool.apply_async(decode, (self.acoustic_model, self.dictionary, self.language_model, audio))
            results.append(result)
            offset += segment_length
        hyps = []
        for result in results:
            hyps.append(result.get(None))
        os.remove(wave_file)
        return ' '.join(hyps)

    def convert(self, audio_file):
        tmp_file = tempfile.NamedTemporaryFile(mode = 'r+b', prefix = 'pocketsphinx_', suffix = '.wav')
        tmp_file_name = tmp_file.name
        tmp_file.close()
        psox = Popen(['sox', audio_file, '-c', '1', '-r', str(self.sample_rate), '-b', str(self.bits), tmp_file_name ])
        psox.wait()
        return tmp_file_name
