# Lilypond File Generator

A ruby program to generate basic score/part skeletons for my lilypond
workflow. 

## Feature Implemented

none yet...

## Feature Goals
* Take input from user about
    * Lilypond version (if it can't be found automatically)
    * language
    * files to include
    * names of different instruments
    * number of movements
    * title composer etc?
* output
    * one part per instrument
    * defs file?
    * one score
    * directory structure?
* output files should have
    * version and language statmen
    * include for a defs file and others if needed
    * variables for each part/movement
    * compile (mostly) cleanly (I don't expect to get all edge cases)

## TODO:
[ ] Create a function to get lilypond version and output version statement
    * find where lilypond version info is on a system generally and look there.
    * run lilypond --version and collect output?
    * collect from user
[ ] Create a function to get language from user and output language statement
[ ] Create a funciton to get includes and output include statement 
[ ] Create a function to get names of instruments, output array
[ ] Create a function to get number of movements, output array of number words

[ ] combine instruments and movement number to get variables needed arrays or
  array of arrays. maybe hash of arrays.
[ ] figure out what files need to be created (array of instruments)
[ ] create parts for each instrument with correct variable (array.each will help
  a lot) and score
    * write in version language includes
    * write in static part-level lines (\book, \paper, etc.)
    * write in static lines for each variable and variable (some kind of each
    loop will be needed.
[ ] write in necessary static lines
  
