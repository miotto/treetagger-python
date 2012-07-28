# treetagger-python

A Python module for interfacing with the Treetagger by Helmut Schmid.

## Dependencies

* [TreeTagger](http://www.ims.uni-stuttgart.de/projekte/corplex/TreeTagger/)
* Python 2.6
* [NLTK](http://nltk.org/)

## INSTALLATION

Before you install the ```treetagger-python``` package please ensure you have downloaded and installed the TreeTagger itself.

The TreeTagger is a copyrighted software by Helmut Schmid and IMS, please read the license agreament before you download the TreeTagger package and language models.

After the installation of the ```TreeTagger``` set the environment variable ```TREETAGGER_HOME``` to the installation directory of the ```TreeTagger```:

    export TREETAGGER_HOME='/path/to/your/TreeTagger/'

## Usage

Tagging a text document from Python:
    
    from treetagger import TreeTagger
    tt = TreeTagger(encoding='latin-1',language='english')
    tt.tag('What is the airspeed of an unladen swallow ?')

