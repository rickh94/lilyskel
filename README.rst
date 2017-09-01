Lilypond Skeletons
==================
.. image:: https://travis-ci.org/rickh94/lyskel.svg?branch=master
    :target: https://travis-ci.org/rickh94/lyskel
.. image:: https://codecov.io/gh/rickh94/lyskel/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/rickh94/lyskel

Generate a file/directory skeleton for lilypond projects.


Features
========
(In progress)

Generates a score, all parts, and a defs file based on information provided by
the user:

* Lilypond version installed (preferably retrieved from lilypond --version)
* Language used for input
* Instruments in the piece

  - Will look up instrument information against a local tinydb database
    (single json file). This database will have Instruments and Ensembles

  - If something is missing, it will be created from user input and can be
    added to the database for future use.

* Composer (in db too?)
* Title
* Subtitle
* Arranger
* Opus
* Copyright information
* Information for Mutopia Project headers (some info in rc file?)
* Number of movements
* Files to include

All configuration will be stored in .lyskel.yaml in the current (or
specified) directory. Users can create them manually or through an
interactive shell (with completion).
