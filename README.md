# Lilypond File Generator

A ruby program to generate basic score/part skeletons for my Lilypond
workflow. 

## Feature Implemented

* Get Lilypond version automatically or from user.
* Get language from user and check against Lilypond supported languages.

## Feature Goals
* Take input from user about
    * ~~Lilypond version (if it can't be found automatically)~~
    * ~~language~~
    * files to include
    * names of different instruments
    * number of movements
    * title composer etc?
* output
    * one part per instrument
    * defs file
    * has usual header fields and mutopia header fields if needed.
    * one score
    * directory structure?
* output files should have
    * version and language statmen
    * include for a defs file and others if needed
    * variables for each part/movement
    * compile (mostly) cleanly (I don't expect to get all edge cases)

