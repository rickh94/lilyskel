# TODO:
* ~~Create a function to get lilypond version and output version statement
    * find where lilypond version info is on a system generally and look there.
    * run lilypond --version and collect output?
    * collect from user ~~ DONE!
* Create a function to get language from user and output language statement
* Create a funciton to get includes and output include statement 
* Create a function to get names of instruments, output array
* Create a function to get number of movements, output array of number words

* combine instruments and movement number to get variables needed arrays or
  array of arrays. maybe hash of arrays.
* figure out what files need to be created (array of instruments)
* create parts for each instrument with correct variable (array.each will help
  a lot) and score
    * write in version language includes
    * write in static part-level lines (\book, \paper, etc.)
    * write in static lines for each variable and variable (some kind of each
    loop will be needed.
* write in necessary static lines
  
