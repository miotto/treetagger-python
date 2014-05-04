treetagger-python
=================

A Python module for interfacing with the Treetagger by Helmut Schmid.

Copyright (C) 2013 Mirko Otto

For license information, see LICENSE.txt

Dependencies
------------

-  `TreeTagger <http://www.ims.uni-stuttgart.de/projekte/corplex/TreeTagger/>`__
-  Python 2.6
-  `NLTK <http://nltk.org/>`__

INSTALLATION
------------

Before you install the ``treetagger-python`` package please ensure you
have downloaded and installed the
`TreeTagger <http://www.ims.uni-stuttgart.de/projekte/corplex/TreeTagger/>`__
itself.

The
`TreeTagger <http://www.ims.uni-stuttgart.de/projekte/corplex/TreeTagger/>`__
is a copyrighted software by Helmut Schmid and
`IMS <http://www.ims.uni-stuttgart.de/>`__, please read the license
agreement before you download the TreeTagger package and language
models.

After the installation of the ``TreeTagger`` set the environment
variable ``TREETAGGER_HOME`` to the installation directory of the
``TreeTagger``.

::

    export TREETAGGER_HOME='/path/to/your/TreeTagger/'

Usage
-----

Tagging a sentence from Python:

::

    from treetagger import TreeTagger
    tt = TreeTagger(encoding='latin-1',language='english')
    tt.tag('What is the airspeed of an unladen swallow?')

The output is a list of [token, tag, lemma]:

::

    [[u'What', u'WP', u'What'],
    [u'is', u'VBZ', u'be'],
    [u'the', u'DT', u'the'],
    [u'airspeed', u'NN', u'airspeed'],
    [u'of', u'IN', u'of'],
    [u'an', u'DT', u'an'],
    [u'unladen', u'JJ', u'<unknown>'],
    [u'swallow', u'NN', u'swallow'],
    [u'?', u'SENT', u'?']]

