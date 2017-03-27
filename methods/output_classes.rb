#!/usr/bin/env ruby
# generate_filenames.rb - combines the headers and instrument to return a
# filenames that need to be created.

require './get_instruments.rb'
# Creating new classes
class Output
  
  def initialize(version, language, headers, instruments)
    @vers = version
    @lang = language
    @heads = headers
    @instrs = instruments
  end

  def name()
    'superceded'
  end

  def filename_prefix()
    # Generate filename prefix from opus or title. Prefer opus.
    @heads.has_key?("opus") ? 
      prefix = @heads['opus'].gsub('Op. ', 'O').tr(' ', '_').upcase :
      prefix = @heads['title'].downcase.tr(' ', '_').gsub('.', '')
    return prefix
  end

  # This will be superceded by subclasses
  def filename()
    'not_sublcass'
  end

  # Create the file.
  def create()
    @file = File.new(filename(), "w")
  end

  # Write the top of the file
  def write_top()
    @file.puts @vers
    @file.puts @lang
    @file.puts "\n#(ly:set-option 'relative-includes #t)"
    @file.puts '\include "defs.ily"'
    @file.puts '\header {'
    @file.puts '  instrument = "' + name() + '"'
    @file.puts "}\n\n"
    @file.puts '\book {'
  end

  # Write the final closing bracket, possibly page info later
  def write_bottom()
    @file.puts '}'
  end

  # close the file
  def done()
    @file.close
  end

end

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

#tests = { "opus" => "Op. 15", "title" => "Test Title"}
##tests_2 = { "title" => "Test Title" }
#score = Score.new("vers", "lang", tests, "instruments")
#score.create()
#score.write_top()
#score.write_bottom()
#score.done()

class Part < Output
  # change initialize
  def initialize(version, language, headers, instrument)
    @vers = version
    @lang = language
    @heads = headers
    @instr = instrument
  end

  def filename()
    filename_prefix() + '_' + @instr.file + '.ly'
  end

  def name()
    @instr.pretty()
  end
end


##tests = { "opus" => "Op. 15", "title" => "Test Title"}
##tests_2 = { "title" => "Test Title" }
#vio = Instrument.new("violin_1")
#part = Part.new("vers", "lang", tests, vio)
#part.create()
#part.write_top()
#part.write_bottom()
#part.done()
