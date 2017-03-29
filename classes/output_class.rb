#!/usr/bin/env ruby
#  output_classes.rb - classes for creation of files: Output and subclasses
#  Score and Part. Generate and write files given inputs.

#require './info_class.rb'

# Creating new classes
class Output
  def initialize(info)
    @vers = info.version
    @lang = info.language
    @heads = info.headers
    @instrs = info.instruments
    @movs = info.movements
  end

  def name()
    # always superceded by subclass. for debugging purposes only.
    'Something in missing in the sublcass name() method'
  end

  def filename_prefix()
    # Generate filename prefix from opus or title. Prefer opus.
    @heads.has_key?("opus") ? 
      prefix = @heads['opus'].gsub(/Op\.\s*/, 'O').tr(' ', '_').upcase :
      prefix = @heads['title'].downcase.tr(' ', '_').gsub('.', '')
    return prefix
  end

  # This will be superceded by subclasses. for debugging only.
  def filename()
    'not_sublcass'
  end

  # Create the file.
  def create()
    @file = File.new(filename(), "w")
  end

  # Write the top of the file
  def write_top()
    @file.puts '\version "' + @vers + '"'
    @file.puts '\language "' + @lang + '"'
    @file.puts "% " + filename() + " - part of " + @heads['title'] + \
      ' by ' + @heads['composer'] + '.'
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

  # for debugging purposes only
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
