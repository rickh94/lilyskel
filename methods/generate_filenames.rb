#!/usr/bin/env ruby
# generate_filenames.rb - combines the headers and instrument to return a
# filenames that need to be created.

# Creating new classes
class Output
  
  def initialize(version, language, headers, instruments)
    @vers = version
    @lang = language
    @heads = headers
    @insts = instruments
  end

  def name()
    'superceded'
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
    # Use opus or title for prefix. Prefer opus.
    @heads.has_key?("opus") ? 
      prefix = @heads['opus'].gsub('Op. ', 'O').tr(' ', '_').upcase :
      prefix = @heads['title'].downcase.tr(' ', '_').gsub('.', '')

    #  Make the score filename
    new_name = Array.new
    new_name << prefix
    new_name << 'score.ly'
    new_name.join('_').to_s
  end

  def name()
    "Score"
  end
end

tests = { "opus" => "Op. 15", "title" => "Test Title"}
score = Score.new("vers", "lang", tests, "instruments")
score.create()
score.write_top()
score.write_bottom()
score.done()

def part_filename(headers, instrument)
  filename = String.new

  #  If there is an opus, use that for the filename prefix, otherwise use the
  #  title.
  headers.has_key?("opus") ? 
    prefix = headers['opus'].gsub('Op. ', 'O').tr(' ', '_').upcase :
    prefix = headers['title'].downcase.tr(' ', '_').gsub('.', '')

  filenames << score_name.join('')

  #  Make filenames for each instrument.
  instruments.each do |ins|
    tmp = Array.new
    tmp << prefix
    tmp << '_' + ins.file.to_s
    tmp << '.ly'
    filenames << tmp.join('')
  end # of instrument filename creator

  # return filenames in array
  filenames
end

