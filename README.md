# Lilypond File Generator

A ruby program to generate basic score/part skeletons for my Lilypond
workflow. 

## Features

Generates a score, all parts, and a defs file based on information provided by
the user:

    * Lilypond version installed (preferably retrieved from lilypond --version)
    * Language used for input
    * Instruments in the piece
    * Composer
    * Title
    * Subtitle
    * Arranger
    * Opus
    * Copyright information
    * Information for Mutopia Project headers
    * Number of movements
    * Files to include

## Future Features

* Generate directory structure
* Create files for note input to variables based on templates 
    * Generate template file
    * Allow user to edit it
    * then generate one file per movement per instrument
