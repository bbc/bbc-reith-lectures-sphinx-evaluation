Evaluation script for CMU Sphinx3 on the BBC Reith Lectures
===========================================================

A set of resources to evaluate Sphinx3 in terms of Word Error Rates on the BBC Reith Lectures.
The Reith lectures are BBC Programmes made available as podcasts along with their transcripts
on the BBC web site, under [personal non-commercial terms of use](http://www.bbc.co.uk/podcasts/help/terms/).
They cover almost each year since 1976 and a wide range of different speakers.

It can therefore be used for the evaluation of multi-speaker Automated Speech Recognition (ASR) system.
In particular, this script helps with evaluating the [CMU Sphinx](http://cmusphinx.sourceforge.net/) 
ASR system, to see how different acoustic and language models compare to each other.

However the transcripts are not verbatim. For example quite a few lectures start
with an introduction of the speaker, which is not available in the transcripts. 
Some times, the speaker deviate from the transcripts as well. Therefore
the results will often be slightly worse than one could expect.


Dependencies
------------

The evaluation script relies on [SoX](http://sox.sourceforge.net/) being installed, and the
PocketSphinx python bindings. 

>  # apt-get install sox libsox-fmt-mp3 python-numpy python-pocketsphinx

Getting started
---------------

Start by downloading the dataset using the provided script.

> $ cd reith-lectures

> $ ../get-reith-lectures-dataset.sh

Create a configuration file pointing to your acoustic and language models. 
An example configuration file is given in hub4\_and\_lm\_giga\_64k\_vp\_3gram.ini.example, using
the HUB4 acoustic model bundled with Sphinx and a [language model derived from the English
Gigaword corpus](http://www.keithv.com/software/giga/).

Run the evaluation.

> $ ./evaluate.py --directory reith-lectures --config sphinx-config.ini

If you want to run the evaluation using only pre-computed transcriptions, use the --lazy flag.

For example to run the evaluation on transcriptions derived using the example configuration file:

> $ ./evaluate.py --directory reith-lectures-hub4-and-lm-giga-64k-vp-3gram --lazy true 

> Average WER: 0.556791

The full results of the above command are available in reith-lectures-hub4-and-lm-giga-64k-vp-3gram/evaluation-results.txt

Licensing terms and authorship
------------------------------

See 'COPYING' and 'AUTHORS' files.
The audio and transcripts are made available on the BBC web site under
[personal non-commercial terms of use](http://www.bbc.co.uk/podcasts/help/terms/)
