# TODO:

__UPDATE README__

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
  
* ~~CHANGE TO CLASS Create instrument class that holds three versions of its name: (file, variable, pretty)~~ DONE!
* ~~Create a function to get number of movements, output array of number
  words~~DONE!
* ~~Create a function to get title, composer, opus, etc. and Mutopia fields for defs.ily~~DONE!
* __CHANGE FUCKING EVERTHING__ In order for it to work properly, everything
  needs to use classes. Current theory:
    * ~~Create Output class with methods create_file, write_top, write middle, write_bottom, and maybe
      some others.~~DONE!
    * ~~Create Defs, Score and Part subclasses~~DONE! with write_score and write_part methods
      (respectively) for more specific things
    * ~~Possibly consolidate info into class.~~DONE!

__All that's left is the hard part__

## Writing Files
* ~~Combine instruments and movement number to get variables needed arrays or
  array of arrays. Maybe hash of arrays.~~Changed my mind.
* ~~Figure out what files need to be created (array of instruments)~~Changed
  my mind.
* Create parts for each instrument with correct variable (array.each will help
  a lot) and score
    * ~~Write in version language includes (defs.ily)~~DONE!
    * ~~Enable relative includes~~DONE!
    * Write in static part-level lines (\book, \paper, etc.)
    * Write in static lines for each variable and variable (some kind of each
    loop will be needed.
* ~~Write in necessary static lines~~DONE!

