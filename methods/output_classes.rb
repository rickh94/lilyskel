#!/usr/bin/env ruby
#  output_classes.rb - classes for creation of files: Output and subclasses
#  Score and Part. Generate and write files given inputs.

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
    @file.puts "% " + filename() + " - part of " + @heads['title'] + '.'
  end
  
  def write_supporting()
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

  def write_middle()
    puts "Something is missing in an Output subclass. fix it"
  end

  def write()
    write_top()
    write_supporting()
    write_middle()
    write_bottom()
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

# TESTS for the Score Class
#tests = { "opus" => "Op. 15", "title" => "Test Title"}
##tests_2 = { "title" => "Test Title" }
#score = Score.new("vers", "lang", tests, "instruments")
#score.create()
#score.write()
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

# TESTS for the Part Class
#tests = { "opus" => "Op. 15", "title" => "Test Title"}
#tests_2 = { "title" => "Test Title" }
#vio = Instrument.new("violin_1")
#part = Part.new("vers", "lang", tests, vio)
#part.create()
#part.write()
#part.done()


class Defs < Output
  # change initialize
  def initialize(version, language, headers)
    @vers = version
    @lang = language
    @heads = headers
    puts 'Please enter the file names you would like to include'\
      'in your Lilypond project, separated by commas:'
    @includes = gets.chomp.to_s.split(',').map{ |i| i.to_s.gsub(/^ /, '') }
  end

  def filename()
    'defs.ily'
  end

  def write_header()
    @file.puts "\n" + '\header {'
    @heads.each { |k, v| @file.puts '  ' + k + ' = "' + v + '"' }
    @file.puts '}'
  end

  def write_includes()
    @file.puts "\n\n#(ly:set-option 'relative-includes #t)"
    @includes.each { |i| @file.puts '\include "' + i + '"' }
  end

  def write_supporting()
    write_header()
    write_includes()
  end

  def write_bottom()
    # this type doesn't have a different closing thing
  end
end

# TESTS for the Defs Class
#tests = { "opus" => "Op. 15", "title" => "Test Title"}
#defs = Defs.new("vers", "lang", tests)
#defs.create()
#defs.write()
#defs.done()
