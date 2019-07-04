# -*- coding: utf-8 -*-
# Natural Language Toolkit: Interface to the TreeTagger POS-tagger
#
# Copyright (C) Mirko Otto
# Author: Mirko Otto <dropsy@gmail.com>

"""
A Python module for interfacing with the Treetagger by Helmut Schmid.
"""

import os, fnmatch, re
from subprocess import Popen, PIPE

from nltk.internals import find_binary, find_file
from nltk.tag.api import TaggerI
from nltk.chunk.api import ChunkParserI
from nltk.tree import Tree
from sys import platform as _platform

_treetagger_url = 'http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/'

def files(path, pattern):
  for file in os.listdir(path):
      if (os.path.isfile(os.path.join(path, file)) and fnmatch.fnmatch(file, pattern)):
          yield file

class TreeTagger(TaggerI):
    r"""
    A class for pos tagging with TreeTagger. The default encoding used by TreeTagger is utf-8. The input is the paths to:
     - a language trained on training data
     - (optionally) the path to the TreeTagger binary

    This class communicates with the TreeTagger binary via pipes.

    Example:

    .. doctest::
        :options: +SKIP

        >>> from treetagger import TreeTagger
        >>> tt = TreeTagger(language='english')
        >>> tt.tag('What is the airspeed of an unladen swallow?')
        [['What', 'WP', 'what'],
         ['is', 'VBZ', 'be'],
         ['the', 'DT', 'the'],
         ['airspeed', 'NN', 'airspeed'],
         ['of', 'IN', 'of'],
         ['an', 'DT', 'an'],
         ['unladen', 'JJ', '<unknown>'],
         ['swallow', 'NN', 'swallow'],
         ['?', 'SENT', '?']]

    .. doctest::
        :options: +SKIP

        >>> from treetagger import TreeTagger
        >>> tt = TreeTagger(language='german')
        >>> tt.tag('Das Haus hat einen großen hübschen Garten.')
        [['Das', 'ART', 'die'],
         ['Haus', 'NN', 'Haus'],
         ['hat', 'VAFIN', 'haben'],
         ['einen', 'ART', 'eine'],
         ['großen', 'ADJA', 'groß'],
         ['hübschen', 'ADJA', 'hübsch'],
         ['Garten', 'NN', 'Garten'],
         ['.', '$.', '.']]
    """


    def __init__(self, path_to_treetagger=None, language='english',
                 verbose=False, abbreviation_list=None):
        """
        Initialize the TreeTagger.

        :param language: Default language is english.

        The encoding used by the model. Unicode tokens
        passed to the tag() method are converted to
        this charset when they are sent to TreeTagger.
        The default is utf-8.

        This parameter is ignored for str tokens, which are sent as-is.
        The caller must ensure that tokens are encoded in the right charset.
        """
        if path_to_treetagger:
            self._path_to_treetagger = path_to_treetagger
        else:
            self._path_to_treetagger = None

        treetagger_paths = ['.']
        if 'TREETAGGER_HOME' in os.environ:
            if _platform.startswith('win'):
                tt_path = os.path.normpath(os.path.join(os.environ['TREETAGGER_HOME'], 'bin'))
            else:
                tt_path = os.path.normpath(os.path.join(os.environ['TREETAGGER_HOME'], 'cmd'))
            treetagger_paths.append(tt_path)
        elif self._path_to_treetagger:
            if _platform.startswith('win'):
                tt_path = os.path.normpath(os.path.join(self._path_to_treetagger, 'bin'))
            else:
                tt_path = os.path.normpath(os.path.join(self._path_to_treetagger, 'cmd'))
            treetagger_paths.append(tt_path)
        else:
            raise LookupError('Set \'TREETAGGER_HOME\' or use path_to_treetagger!')
        treetagger_paths = list(map(os.path.expanduser, treetagger_paths))

        self._abbr_list = abbreviation_list

        if language in self.get_installed_lang():
            if _platform.startswith('win'):
                treetagger_bin_name = 'tag-' + language + '.bat'
            else:
                treetagger_bin_name = 'tree-tagger-' + language
        else:
            raise LookupError('Language not installed!')

        try:
            self._treetagger_bin = find_binary(
                treetagger_bin_name,
                searchpath=treetagger_paths,
                url=_treetagger_url,
                verbose=verbose)
        except LookupError:
            print('NLTK was unable to find the TreeTagger bin!')

    def get_treetagger_path(self):
        if 'TREETAGGER_HOME' in os.environ:
            print('Environment variable \'TREETAGGER_HOME\' is ' + os.environ['TREETAGGER_HOME'])
        else:
            print('Environment variable \'TREETAGGER_HOME\' not set')

        if self._path_to_treetagger:
            print('Path to TreeTagger is ' + self._path_to_treetagger)
        else:
            print('Path to TreeTagger not set')

    def get_installed_lang(self):
        if 'TREETAGGER_HOME' in os.environ:
            lang_path = os.path.normpath(os.path.join(os.environ['TREETAGGER_HOME'], 'lib'))
            return [file[:-4] for file in files(lang_path, "*.par") if not file.endswith("chunker.par")]
        elif self._path_to_treetagger:
            lang_path = os.path.normpath(os.path.join(self._path_to_treetagger, 'lib'))
            return [file[:-4] for file in files(lang_path, "*.par") if not file.endswith("chunker.par")]
        else:
            return []

    def tag(self, sentences):
        """Tags a single sentence: a list of words.
        The tokens should not contain any newline characters.
        """

        # Write the actual sentences to the temporary input file
        if isinstance(sentences, list):
            _input = '\n'.join((x for x in sentences))
        else:
            _input = sentences

        # Run the tagger and get the output
        if(self._abbr_list is None):
            p = Popen([self._treetagger_bin],
                        shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        elif(self._abbr_list is not None):
            p = Popen([self._treetagger_bin,"-a",self._abbr_list],
                        shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)

        (stdout, stderr) = p.communicate(str(_input).encode('utf-8'))

        # Check the return code.
        if p.returncode != 0:
            print(stderr)
            raise OSError('TreeTagger command failed!')

        treetagger_output = stdout.decode('UTF-8')

        # Output the tagged sentences
        tagged_sentences = []
        for tagged_word in treetagger_output.strip().split('\n'):
            tagged_word_split = tagged_word.split('\t')
            tagged_sentences.append(tagged_word_split)

        return tagged_sentences

class TreeTaggerChunker(ChunkParserI):
    r"""
    A class for chunking with TreeTagger Chunker. The default encoding used by TreeTagger is utf-8. The input is the paths to:
     - a language trained on training data
     - (optionally) the path to the TreeTagger binary

    This class communicates with the TreeTagger Chunker binary via pipes.

    Example:

    .. doctest::
        :options: +SKIP

        >>> from treetagger import TreeTaggerChunker
        >>> tt = TreeTaggerChunker(language='english')
        >>> tt.parse('What is the airspeed of an unladen swallow?')
        [['<NC>'], ['What', 'WP', 'what'], ['</NC>'], ['<VC>'], ['is', 'VBZ', 'be'], ['</VC>'], ['<NC>'], ['the', 'DT', 'the'], ['airspeed', 'NN', 'airspeed'], ['</NC>'], ['<PC>'], ['of', 'IN', 'of'], ['<NC>'], ['an', 'DT', 'an'], ['unladen', 'JJ', '<unknown>'], ['swallow', 'NN', 'swallow'], ['</NC>'], ['</PC>'], ['?', 'SENT', '?']]

    .. doctest::
        :options: +SKIP

        >>> from treetagger import TreeTaggerChunker
        >>> tt = TreeTaggerChunker(language='english')
        >>> tt.parse_to_tree('What is the airspeed of an unladen swallow?')
        Tree('S', [Tree('NC', [Tree('What', ['WP'])]), Tree('VC', [Tree('is', ['VBZ'])]), Tree('NC', [Tree('the', ['DT']), Tree('airspeed', ['NN'])]), Tree('PC', [Tree('of', ['IN']), Tree('NC', [Tree('an', ['DT']), Tree('unladen', ['JJ']), Tree('swallow', ['NN'])])]), Tree('?', ['SENT'])])

    .. doctest::
        :options: +SKIP

        >>> from nltk.tree import Tree
        >>> from treetagger import TreeTaggerChunker
        >>> tt = TreeTaggerChunker(language='english')
        >>> res = tt.parse_to_tree('What is the airspeed of an unladen swallow?')
        >>> print(res)
        (S
          (NC (What WP))
          (VC (is VBZ))
          (NC (the DT) (airspeed NN))
          (PC (of IN) (NC (an DT) (unladen JJ) (swallow NN)))
          (? SENT))
    """

    def __init__(self, path_to_treetagger=None, language='english',
                 verbose=False, abbreviation_list=None):
        """
        Initialize the TreeTaggerChunker.

        :param language: Default language is english.

        The encoding used by the model. Unicode tokens
        passed to the parse() and parse_to_tree() methods are converted to
        this charset when they are sent to TreeTaggerChunker.
        The default is utf-8.

        This parameter is ignored for str tokens, which are sent as-is.
        The caller must ensure that tokens are encoded in the right charset.
        """
        if path_to_treetagger:
            self._path_to_treetagger = path_to_treetagger
        else:
            self._path_to_treetagger = None

        treetagger_paths = ['.']
        if 'TREETAGGER_HOME' in os.environ:
            if _platform.startswith('win'):
                tt_path = os.path.normpath(os.path.join(os.environ['TREETAGGER_HOME'], 'bat'))
            else:
                tt_path = os.path.normpath(os.path.join(os.environ['TREETAGGER_HOME'], 'cmd'))
            treetagger_paths.append(tt_path)
        elif self._path_to_treetagger:
            if _platform.startswith('win'):
                tt_path = os.path.normpath(os.path.join(self._path_to_treetagger, 'bat'))
            else:
                tt_path = os.path.normpath(os.path.join(self._path_to_treetagger, 'cmd'))
            treetagger_paths.append(tt_path)
        else:
            raise LookupError('Set \'TREETAGGER_HOME\' or use path_to_treetagger!')
        treetagger_paths = list(map(os.path.expanduser, treetagger_paths))

        self._abbr_list = abbreviation_list

        if language in self.get_installed_lang():
            if _platform.startswith('win'):
                treetagger_chunker_bin_name = 'chunk-' + language + '.bat'
            else:
                treetagger_chunker_bin_name = 'tagger-chunker-' + language
        else:
            raise LookupError('Language not installed!')

        try:
            self._treetagger_chunker_bin = find_binary(
                treetagger_chunker_bin_name,
                searchpath=treetagger_paths,
                url=_treetagger_url,
                verbose=verbose)
        except LookupError:
            print('NLTK was unable to find the TreeTagger Chunker bin!')

    def get_treetagger_path(self):
        if 'TREETAGGER_HOME' in os.environ:
            print('Environment variable \'TREETAGGER_HOME\' is ' + os.environ['TREETAGGER_HOME'])
        else:
            print('Environment variable \'TREETAGGER_HOME\' not set')

        if self._path_to_treetagger:
            print('Path to TreeTagger is ' + self._path_to_treetagger)
        else:
            print('Path to TreeTagger not set')

    def get_installed_lang(self):
        if 'TREETAGGER_HOME' in os.environ:
            lang_path = os.path.normpath(os.path.join(os.environ['TREETAGGER_HOME'], 'lib'))
            lang_files = [file[:-4] for file in files(lang_path, "*.par")]
            lang_chunk_files = [file[:-12] for file in files(lang_path, "*-chunker.par")]
            return [item for item in lang_chunk_files if item in lang_files]
        elif self._path_to_treetagger:
            lang_path = os.path.normpath(os.path.join(self._path_to_treetagger, 'lib'))
            lang_files = [file[:-4] for file in files(lang_path, "*.par")]
            lang_chunk_files = [file[:-12] for file in files(lang_path, "*-chunker.par")]
            return [item for item in lang_chunk_files if item in lang_files]
        else:
            return []

    def parse(self, tokens):
        """Tag and chunk a single sentence: a list of words.
        The tokens should not contain any newline characters.
        """

        # Write the actual sentences to the temporary input file
        if isinstance(tokens, list):
            _input = '\n'.join((x for x in tokens))
        else:
            _input = tokens

        # Run the tagger chunker and get the output
        if(self._abbr_list is None):
            p = Popen([self._treetagger_chunker_bin],
                        shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        elif(self._abbr_list is not None):
            p = Popen([self._treetagger_chunker_bin,"-a",self._abbr_list],
                        shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)

        (stdout, stderr) = p.communicate(str(_input).encode('utf-8'))

        # Check the return code.
        if p.returncode != 0:
            print(stderr)
            raise OSError('TreeTaggerChunker command failed!')

        treetagger_chunker_output = stdout.decode('UTF-8')

        # Output the tagged ans chunked sentences
        tagged_chunked_sentences = []
        for tagged_word in treetagger_chunker_output.strip().split('\n'):
            tagged_word_split = tagged_word.split('\t')
            tagged_chunked_sentences.append(tagged_word_split)

        return tagged_chunked_sentences

    def parse_to_tree(self, tokens):
        tc_sentences = self.parse(tokens)

        resar = []
        res = ''
        for idx, item in enumerate(tc_sentences):
            if len(item) == 1:
                erg  = re.sub('</[a-zA-Z]*>',')',item[0])
                if erg == ')':
                    res += erg
                else:
                    erg1 = re.sub('<',' (',item[0])
                    erg2 = re.sub('>','',erg1)
                    res += erg2

            if len(item) == 3:
                res += ' ('+item[0]+' '+item[1] +')'
                if item[1] == 'SENT' or item[1] == '$.' or item[1] == 'FS':
                    res = '(S '+res+')'
                    resar.append(res)
                    res = ''

            if len(tc_sentences)==idx+1 and len(res) > 1 and res[0:2] != '(S':
                res = '(S '+res+')'
                resar.append(res)
                res = ''

        if len(resar) > 1:
            erg = '(ROOT '+' '.join(resar)+')'
        else:
            erg = resar[0]

        try:
            return Tree.fromstring(erg)
        except ValueError:
             print('Something goes wrong. Please check the raw data:\n')
             print(erg)


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
