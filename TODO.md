# TODO:
* ~~Create a function to get lilypond version and output version statement~~DONE!
    * ~~find where lilypond version info is on a system generally and look there~~
    * ~~run lilypond --version and collect output?~~
    * ~~collect from user~~ 
* ~~Create a function to get language from user and output language
  statement~~DONE!
* Create a funciton to get includes and output include statement 
* Create a function to get names of instruments, output array
    function for normalizing ary.map{ |x| x.to_s.tr(' A-Z', '_a-z')
    also need to map numbers and numerals to number words for variables and
      numerals to numbers for part names
* Create a function to get number of movements, output array of number words
* Create a function to get title, composer, opus, etc. for defs.ily

* combine instruments and movement number to get variables needed arrays or
  array of arrays. maybe hash of arrays.
* figure out what files need to be created (array of instruments)
* create parts for each instrument with correct variable (array.each will help
  a lot) and score
    * write in version language includes (defs.ily)
    * enable relative includes
    * write in static part-level lines (\book, \paper, etc.)
    * write in static lines for each variable and variable (some kind of each
    loop will be needed.
* write in necessary static lines
  
