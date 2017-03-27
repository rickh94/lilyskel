# TODO:

## Needed functions
* ~~Create a function to get lilypond version and output version statement~~DONE!
    * ~~Find where lilypond version info is on a system generally and look there~~
    * ~~Run lilypond --version and collect output?~~
    * ~~collect from user~~ 
* ~~Create a function to get language from user and output language
  statement~~DONE!
* ~~Create a function to get includes and output include statement~~DONE!
* ~~Create a function to get names of instruments, output array~~DONE!(but
  messy)
* ~~__CHANGE TO CLASS__ Create instrument class that holds three versions of its name: (file, variable, pretty)~~DONE!
* ~~Create a function to get number of movements, output array of number
  words~~DONE!
* ~~Create a function to get title, composer, opus, etc. and Mutopia fields for defs.ily~~DONE!

## Writing Files
* Combine instruments and movement number to get variables needed arrays or
  array of arrays. Maybe hash of arrays.
* ~~Figure out what files need to be created (array of instruments)~~DONE!
* Create parts for each instrument with correct variable (array.each will help
  a lot) and score
    * Write in version language includes (defs.ily)
    * Enable relative includes
    * Write in static part-level lines (\book, \paper, etc.)
    * Write in static lines for each variable and variable (some kind of each
    loop will be needed.
* Write in necessary static lines
