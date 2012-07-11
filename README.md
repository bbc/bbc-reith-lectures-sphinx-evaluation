Evaluation of Sphinx on the BBC Reith Lectures
==============================================

A set of resources to evaluate Sphinx3 in terms of Word Error Rates on the BBC Reith Lectures.

Getting started
---------------

Start by downloading the dataset using the provided script.

> $ mkdir reith-lectures && cd reith-lectures
> $ ../get-reith-lectures-dataset.sh

Create a configuration file pointing to your acoustic and language models. 
An example configuration file is given in hub4\_and\_lm\_giga\_64k\_vp\_3gram.ini.example.

Run the evaluation.

> $ ./evaluate.py --directory reith-lectures sphinx-config.ini

If you want to run the evaluation using only pre-computed transcriptions, use the --lazy flag.

Licensing terms and authorship
------------------------------

See 'COPYING' and 'AUTHORS' files.
