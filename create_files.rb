#!/usr/bin/env ruby
# create_files.rb - takes input of filenames and creates one file of each and
# writes [some stuff] into them.

# programatically requires all the methods needed to create the files
Dir[File.dirname(__FILE__) + '/methods/*.rb'].each { |file| require file }

def write_defs_file(version, language, headers, includes)
  defs = File.new("defs.ily", "w")
  defs.puts version
  defs.puts language
  defs.puts '\header {'
  headers.each { |k, v| defs.puts '  ' + k.to_s + ' = "' + v.to_s + '"'}
  defs.puts "}\n\n"
  defs.puts "#(ly:set-option 'relative-includes #t)"
  includes.each { |a| defs.puts a }
end

def write_files(file_names, version, language)
  file_names.each do |file_name|
    new_file = File.new(file_name, "w")
    new_file.puts version
    new_file.puts language
  end
end

vers = get_version()
lang = get_language()
instr = get_instruments()
head = get_headers(instr)
incl = get_includes()
files = generate_filenames(head, instr)
write_defs_file(vers, lang, head, incl)
write_files(files, version, language)
