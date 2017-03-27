#!/usr/bin/env ruby
# create_files.rb - takes input of filenames and creates one file of each and
# writes [some stuff] into them.

# programatically requires all the methods needed to create the files
Dir[File.dirname(__FILE__) + '/methods/*.rb'].each { |file| require file }

def write_defs_file(version, language, headers, includes)
  # Make the defs file
  defs = File.new("defs.ily", "w")

  # Put in version and language
  defs.puts version
  defs.puts language

  # Put in headers
  defs.puts '\header {'
  headers.each { |k, v| defs.puts '  ' + k.to_s + ' = "' + v.to_s + '"'}
  defs.puts "}\n\n"

  # Put in includes
  defs.puts "#(ly:set-option 'relative-includes #t)"
  includes.each { |a| defs.puts a }
end

def write_top(file, version, language, instrument)
  file.puts version
  file.puts language
  file.puts "\n#(ly:set-option 'relative-includes #t)"
  file.puts '\include "defs.ily"' + "\n\n"
  file.puts '\header {'
  file.puts 'instrument = ' + instrument + '"'
  file.puts "}\n\n"
  file.puts '\book {'
end

def write_score(version, language, headers, instruments)
  # Create score file
  file_name = score_filename(headers)
  score_file = File.new(file_name, "w")

  # Write top part of score file
  write_top(score_file, version, language, "Score")
end

#def write_parts(version, language, headers, instruments)

    #part_file = File.new(CHANGEME, "w")
    #write_top(part_file, version, language)

#end

vers = get_version()
lang = get_language()
instr = get_instruments()
head = get_headers(instr)
incl = get_includes()
#files = generate_filenames(head, instr)
write_defs_file(vers, lang, head, incl)
#write_files(files, version, language)
write_score(vers, lang, head, instr)
