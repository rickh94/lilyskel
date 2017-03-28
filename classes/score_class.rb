#!/usr/bin/env ruby
#  output_classes.rb - classes for creation of files: Output and subclasses
#  Score and Part. Generate and write files given inputs.


class Score < Output
  # Filename generation for Score.
  def filename()
    #  Make the score filename
    filename_prefix() + '_score.ly'
  end

  def name()
    "Score"
  end
end

# TESTS for the Score Class
#tests = { "opus" => "Op. 15", "title" => "Test Title"}
##tests_2 = { "title" => "Test Title" }
#score = Score.new("vers", "lang", tests, "instruments")
#score.create()
#score.write()
#score.done()

