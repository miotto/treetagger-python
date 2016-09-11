treetagger-python
=================

A Python module for interfacing with the Treetagger by Helmut Schmid.

Copyright (C) 2016 Mirko Otto

For license information, see LICENSE.txt

Dependencies
------------

-  `TreeTagger <http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/>`__
-  Python 3
-  `NLTK <http://nltk.org/>`__
-  treetagger.py is for Python 3
-  treetagger_python2.py is for old Python 2

Tested with Treetagger 3.2, Python 3.4 and NLTK 3.0.4

INSTALLATION
------------

Before you install the ``treetagger-python`` package please ensure you
have downloaded and installed the
`TreeTagger <http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/>`__
itself.

The
`TreeTagger <http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/>`__
is a copyrighted software by Helmut Schmid and
`IMS <http://www.ims.uni-stuttgart.de/>`__, please read the license
agreement before you download the TreeTagger package and language
models.

After the installation of the ``TreeTagger`` set the environment
variable ``TREETAGGER_HOME`` to the installation directory of the
``TreeTagger``.

::

    export TREETAGGER_HOME='/path/to/your/TreeTagger/cmd/'

Usage
-----

Tagging a sentence from Python:

::

    from treetagger import TreeTagger
    tt = TreeTagger(language='english')
    tt.tag('What is the airspeed of an unladen swallow?')

The output is a list of [token, tag, lemma]:

::

    [['What', 'WP', 'What'], 
    ['is', 'VBZ', 'be'], 
    ['the', 'DT', 'the'], 
    ['airspeed', 'NN', 'airspeed'], 
    ['of', 'IN', 'of'], 
    ['an', 'DT', 'an'], 
    ['unladen', 'JJ', '<unknown>'], 
    ['swallow', 'NN', 'swallow'], 
    ['?', 'SENT', '?']]

Tagging a german sentence from Python:

::

    from treetagger import TreeTagger
    tt = TreeTagger(language='german')
    tt.tag('Das Haus hat einen großen hübschen Garten.')

The output is a list of [token, tag, lemma]:

::

    [['Das', 'ART', 'die'], 
    ['Haus', 'NN', 'Haus'], 
    ['hat', 'VAFIN', 'haben'], 
    ['einen', 'ART', 'eine'], 
    ['großen', 'ADJA', 'groß'], 
    ['hübschen', 'ADJA', 'hübsch'], 
    ['Garten', 'NN', 'Garten'], 
    ['.', '$.', '.']]
