treetagger-python
=================

A Python module for interfacing with the Treetagger by Helmut Schmid.

Copyright (C) 2018 Mirko Otto

For license information, see LICENSE.txt

Dependencies
------------

-  `TreeTagger <http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/>`__ (The names of the parametres Files of the TreeTagger program have changed, use the version after the 16th of October 2018; Since October 2020, it seems that the data must now be transferred to the TreeTagger programme as files.)
-  Python 3
-  `NLTK <http://nltk.org/>`__
-  treetagger.py is for Python 3

Tested in June 2021 with TreeTagger 3.2.3 (versions after October 2020), Python 3.9.5 and NLTK 3.6.2 on Ubuntu 20.04, OSX 10.15 and Windows 10

Preparation
------------

The
`TreeTagger <http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/>`__
is a copyrighted software by Helmut Schmid and
`IMS <http://www.ims.uni-stuttgart.de/>`__, please read the license
agreement before you download the TreeTagger package and language
models.

Before you can use the ``treetagger-python`` package please ensure you
have downloaded and installed the
`TreeTagger <http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/>`__
itself.

After installing the ``TreeTagger`` program, please check if it works properly. 

The ``treetagger-python`` package now checks the installed language packs "language-utf8.par" in the ``lib`` directory. You can use the ``get_installed_lang`` function to show the languages. The corresponding executable files are used in the ``cmd`` directory under Linux and in the ``bat`` directory under Windows.

The English tagging examples and the Python doctest show the result with the "English parameter file (PENN tagset)" file.

Installation
-----------

Make sure that you know the HOME directory of the TreeTagger program.

To use the Python package ``treetagger-python``, you must either set the environment variable ``TREETAGGER_HOME`` or the path ``path_to_treetagger`` when the program is called. In section usage you can see the second option.

To set the environment variable ``TREETAGGER_HOME``, enter the path to the installation directory of ``TreeTagger``:

::

    export TREETAGGER_HOME='/path/to/your/TreeTagger/'


Clone the repository and change to this directory. In this directory the Python package ``treetagger-python`` can be used without installation.:

::

    clone https://github.com/miotto/treetagger-python.git
    cd treetagger-python

Usage
-----

Initialize by specifying the path ``path_to_treetagger``:

::

    from treetagger import TreeTagger
    tt = TreeTagger(path_to_treetagger='/path/to/your/TreeTagger/')

Usage TreeTagger
^^^^^^^^^^^^^^^^

Show the installed languages:

::

    from treetagger import TreeTagger
    tt = TreeTagger(path_to_treetagger='/path/to/your/TreeTagger/')
    tt.get_installed_lang()

The output could look like this

::

    ['english', 'german']

Tagging a sentence from Python:

::

    from treetagger import TreeTagger
    tt = TreeTagger(path_to_treetagger='/path/to/your/TreeTagger/')
    tt.tag('What is the airspeed of an unladen swallow?')


The output is a list of [token, tag, lemma]:

::

    [['What', 'WP', 'what'], 
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
    tt = TreeTagger(path_to_treetagger='/path/to/your/TreeTagger/', language='german')
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

Usage TreeTaggerChunker
^^^^^^^^^^^^^^^^^^^^^^^

Initialize by specifying the path ``path_to_treetagger``:

::

    from treetagger import TreeTaggerChunker
    ttc = TreeTaggerChunker(path_to_treetagger='/path/to/your/TreeTagger/')

Show the installed languages:

::

    from treetagger import TreeTaggerChunker
    ttc = TreeTaggerChunker(path_to_treetagger='/path/to/your/TreeTagger/')
    ttc.get_installed_lang()

The output could look like this

::

    ['english', 'german']

Chunk a sentence from Python:

::

    from treetagger import TreeTaggerChunker
    ttc = TreeTaggerChunker(path_to_treetagger='/path/to/your/TreeTagger/')
    ttc.parse('What is the airspeed of an unladen swallow?')


The output is a list of a chunk structure with [token, tag, lemma]:

::

    [['<NC>'], ['What', 'WP', 'what'], ['</NC>'], ['<VC>'], ['is', 'VBZ', 'be'], ['</VC>'], ['<NC>'], ['the', 'DT', 'the'], ['airspeed', 'NN', 'airspeed'], ['</NC>'], ['<PC>'], ['of', 'IN', 'of'], ['<NC>'], ['an', 'DT', 'an'], ['unladen', 'JJ', '<unknown>'], ['swallow', 'NN', 'swallow'], ['</NC>'], ['</PC>'], ['?', 'SENT', '?']]

Chunk a sentence in a tree from Python:

::

    from treetagger import TreeTaggerChunker
    ttc = TreeTaggerChunker(path_to_treetagger='/path/to/your/TreeTagger/')
    ttc.parse_to_tree('What is the airspeed of an unladen swallow?')


The output is a chunk structure as a nltk tree:

::

    Tree('S', [Tree('NC', [Tree('What', ['WP'])]), Tree('VC', [Tree('is', ['VBZ'])]), Tree('NC', [Tree('the', ['DT']), Tree('airspeed', ['NN'])]), Tree('PC', [Tree('of', ['IN']), Tree('NC', [Tree('an', ['DT']), Tree('unladen', ['JJ']), Tree('swallow', ['NN'])])]), Tree('?', ['SENT'])])

Chunk a sentence in a tree from Python:

::

    from nltk.tree import Tree
    from treetagger import TreeTaggerChunker
    ttc = TreeTaggerChunker(path_to_treetagger='/path/to/your/TreeTagger/')
    ttc_tree = ttc.parse_to_tree('What is the airspeed of an unladen swallow?')
    print(ttc_tree)


The output is a chunk structure as a nltk tree:

::

    (S
      (NC (What WP))
      (VC (is VBZ))
      (NC (the DT) (airspeed NN))
      (PC (of IN) (NC (an DT) (unladen JJ) (swallow NN)))
      (? SENT))

