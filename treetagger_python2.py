# -*- coding: utf-8 -*-
# Natural Language Toolkit: Interface to the TreeTagger POS-tagger
#
# Copyright (C) Mirko Otto
# Author: Mirko Otto <dropsy@gmail.com>

"""
A Python module for interfacing with the Treetagger by Helmut Schmid.
"""

import os
from subprocess import Popen, PIPE

from nltk.internals import find_binary, find_file
from nltk.tag.api import TaggerI

def tUoB(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj

_treetagger_url = 'http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/'

_treetagger_languages = {
u'latin-1':['latin', 'latinIT', 'mongolian', 'swahili'],
u'utf-8' : ['bulgarian', 'dutch', 'english', 'estonian', 'finnish', 'french', 'galician', 'german', 'italian', 'polish', 'russian', 'slovak', 'slovak2', 'spanish']}

"""The default encoding used by TreeTagger: utf-8. u'' means latin-1; ISO-8859-1"""
_treetagger_charset = [u'utf-8', u'latin-1']

class TreeTagger(TaggerI):
    ur"""
    A class for pos tagging with TreeTagger. The input is the paths to:
     - a language trained on training data
     - (optionally) the path to the TreeTagger binary
     - (optionally) the encoding of the training data (default: utf-8)

    This class communicates with the TreeTagger binary via pipes.

    Example:

    .. doctest::
        :options: +SKIP

        >>> from treetagger import TreeTagger
        >>> tt = TreeTagger(encoding='utf-8',language='english')
        >>> tt.tag(u'What is the airspeed of an unladen swallow ?')
        [[u'What', u'WP', u'What'],
         [u'is', u'VBZ', u'be'],
         [u'the', u'DT', u'the'],
         [u'airspeed', u'NN', u'airspeed'],
         [u'of', u'IN', u'of'],
         [u'an', u'DT', u'an'],
         [u'unladen', u'JJ', u'<unknown>'],
         [u'swallow', u'NN', u'swallow'],
         [u'?', u'SENT', u'?']]

    .. doctest::
        :options: +SKIP

        >>> from treetagger import TreeTagger
        >>> tt = TreeTagger()
        >>> tt.tag(u'Das Haus ist sehr schön und groß. Es hat auch einen hübschen Garten.')
        [[u'Das', u'ART', u'd'],
         [u'Haus', u'NN', u'Haus'],
         [u'ist', u'VAFIN', u'sein'],
         [u'sehr', u'ADV', u'sehr'],
         [u'sch\xf6n', u'ADJD', u'sch\xf6n'],
         [u'und', u'KON', u'und'],
         [u'gro\xdf', u'ADJD', u'gro\xdf'],
         [u'.', u'$.', u'.'],
         [u'Es', u'PPER', u'es'],
         [u'hat', u'VAFIN', u'haben'],
         [u'auch', u'ADV', u'auch'],
         [u'einen', u'ART', u'ein'],
         [u'h\xfcbschen', u'ADJA', u'h\xfcbsch'],
         [u'Garten', u'NN', u'Garten'],
         [u'.', u'$.', u'.']]
    """

    def __init__(self, path_to_home=None, language='german', 
                 encoding='utf-8', verbose=False, abbreviation_list=None):
        """
        Initialize the TreeTagger.

        :param path_to_home: The TreeTagger binary.
        :param language: Default language is german.
        :param encoding: The encoding used by the model. Unicode tokens
            passed to the tag() and batch_tag() methods are converted to
            this charset when they are sent to TreeTagger.
            The default is utf-8.

            This parameter is ignored for str tokens, which are sent as-is.
            The caller must ensure that tokens are encoded in the right charset.
        """
        treetagger_paths = ['.', '/usr/bin', '/usr/local/bin', '/opt/local/bin',
                        '/Applications/bin', '~/bin', '~/Applications/bin',
                        '~/work/TreeTagger/cmd', '~/tree-tagger/cmd']
        treetagger_paths = map(os.path.expanduser, treetagger_paths)
        self._abbr_list = abbreviation_list

        try:
            if encoding in _treetagger_languages.keys() and language in _treetagger_languages[encoding]:
                if encoding == u'latin-1':
                    self._encoding = u'latin-1'
                else:
                    self._encoding = encoding
                treetagger_bin_name = 'tree-tagger-' + language

            else:
                raise LookupError('NLTK was unable to find the TreeTagger bin!')
        except KeyError as e:
                raise LookupError('NLTK was unable to find the TreeTagger bin!')

        self._treetagger_bin = find_binary(
                treetagger_bin_name, path_to_home,
                env_vars=('TREETAGGER', 'TREETAGGER_HOME'),
                searchpath=treetagger_paths,
                url=_treetagger_url,
                verbose=verbose)

    def tag(self, sentences):
        """Tags a single sentence: a list of words.
        The tokens should not contain any newline characters.
        """
        encoding = self._encoding

        # Write the actual sentences to the temporary input file
        if isinstance(sentences, list):
            _input = '\n'.join((x for x in sentences))
        else:
            _input = sentences

        if isinstance(_input, unicode) and encoding:
            _input = _input.encode(encoding)

        # Run the tagger and get the output
        if(self._abbr_list is None):
            p = Popen([self._treetagger_bin], 
                        shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        elif(self._abbr_list is not None):
            p = Popen([self._treetagger_bin,"-a",self._abbr_list], 
                        shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        
        (stdout, stderr) = p.communicate(_input)

        # Check the return code.
        if p.returncode != 0:
            print stderr
            raise OSError('TreeTagger command failed!')

        if isinstance(stdout, unicode) and encoding:
            treetagger_output = stdout.decode(encoding)
        else:
            treetagger_output = tUoB(stdout)

        # Output the tagged sentences
        tagged_sentences = []
        for tagged_word in treetagger_output.strip().split('\n'):
            tagged_word_split = tagged_word.split('\t')
            tagged_sentences.append(tagged_word_split)

        return tagged_sentences


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
