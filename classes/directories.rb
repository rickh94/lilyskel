#!/usr/bin/env ruby
# directories.rb - Class for directory creation (and population).

# NOTE: it may be cleaner to split includes into a class but I don't feel like
# it right now.

class Directories

  @@include_files = []

  # creates each directory
  def create(instrument)
    Dir.mkdir(@cd + '/' + instrument.file)
  end

  # makes global files/vars for universal markings
  def make_globals()
    i = 1

    # make directory
    Dir.mkdir(@cd + '/global')

    # make include file
    includes = make_include("global")
    #includes.puts "#(ly:set-option 'relative-includes #t)"
    # make each global file
    while i <= @movements.count
      # make file and add headers
      file_name = 'global_' + i.to_s + '.ily'
      tmp = File.new(@cd + '/global/' + file_name, "w")
      file_top(tmp)
      # make the variable
      tmp.puts "\n\n" + 'global_' + @movements.movement_number(i) + ' = {'
      tmp.puts '}'
      tmp.close()
      # add file to includes file
      includes.puts '\include "global/' + file_name + '"'
      i += 1
    end
  end

  # add common headers to each file
  def file_top(file)
    file.puts '\version "' + @version + '"'
    file.puts '\language "' + @language + '"'
    file.puts ''
  end

  # add variable to instrument files and get user input for additional stuff
  def put_var(file, instrument, i)
    file.puts "\n\n" + instrument.var + '_' + @movements.movement_number(i) \
      + ' = \relative {'
    puts "Please enter additional text for the variable secion of " + instrument.pretty + " mov " + i.to_s + " notes file:"
    puts "(empty line to exit)"
    # grab any number of lines to put in variable section of a file
    loop do
      tmp = gets.chomp.to_s
      break if tmp == ''
      file.puts tmp
    end
    file.puts '}'
  end

  # make include file for a directory
  def make_include(dir_name)
    include_name = dir_name + "_include.ily"
    @@include_files << include_name
    tmp = File.new(@cd + '/' + include_name, "w")
    # add headers to file
    file_top(tmp)
    # set relative includes
    tmp.puts "#(ly:set-option 'relative-includes #t)"
    return tmp
  end

  # make instrument files
  def make_files(instrument)
    i = 1
    # make include file
    includes = make_include(instrument.file)
    while i <= @movements.count
      # make instrument file
      file_name = instrument.file + '/' + instrument.file + '_' + i.to_s + '.ily'
      ins_file = File.new(@cd + '/' + file_name, "w")
      # add headers
      file_top(ins_file)
      # add variable
      put_var(ins_file, instrument, i)
      ins_file.close()
      # add file to includes file
      includes.puts '\include "' + file_name + '"'
      i += 1
    end
  end

  # add include statements for directory include files to defs file
  def include_includes()
    defs = File.open("defs.ily", "a")
    @@include_files.each do |file|
      defs.puts '\include "' + file + '"'
    end
  end

  # main method that calls everything
  def make_all()
    make_globals()
    @instruments.each do |ins|
      create(ins)
      make_files(ins)
    end
    include_includes()
  end

  def initialize(info)
    @cd = Dir.pwd
    @instruments = info.instruments
    @version = info.version
    @movements = info.movements
    @language = info.language
  end

end

   
