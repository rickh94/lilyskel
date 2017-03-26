# Lilypond File Generator

A ruby program to generate basic score/part skeletons for my Lilypond
workflow. 

## Features Implemented

* Get Lilypond version automatically or from user.
* Get language from user and check against Lilypond supported languages.

## Feature Goals
* Take input from user about
    * ~~Lilypond version (if it can't be found automatically)~~
    * ~~Language~~
    * Files to include
    * Names of different instruments
    * Number of movements
    * Title composer etc?
* Output
    * One part per instrument
    * Defs file
    * Has usual header fields and Mutopia header fields if needed.
    * One score
    * Directory structure?
* Output files should have
    * Version and language statement
    * Include for a defs file and others if needed
    * Variables for each part/movement
    * Compile (mostly) cleanly (I don't expect to get all edge cases)

