#!/usr/bin/env ruby
# directories.rb - Class for directory creation (and population).

class Directories

  # creates each directory
  def create(instrument)
    Dir.mkdir(@cd + '/' + instrument.file)
  end

  def make_globals()
    i = 1
    Dir.mkdir(@cd + '/global')
    while i <= @movements.count
      file_prefix = @cd + '/global/global'
      tmp = File.new(file_prefix + '_' + i.to_s + '.ily', "w")
      tmp.puts '\version "' + @version + '"'
      tmp.puts '\language "' + @language + '"'
      tmp.puts "\n\n\n" + 'global_' + @movements.movement_number(i) + ' = {'
      tmp.puts '}'
      tmp.close()
      i += 1
    end
  end

  def file_top(file)
    file.puts '\version "' + @version + '"'
    file.puts '\language "' + @language + '"'
    file.puts ''
  end

  def put_var(file)
    file.puts "\n\n" + instrument.var + '_' + @movements.movement_number(i) \
      + ' = \relative {'
    puts "Please enter additional text for the variable secion of " + instrument.pretty + " mov " + i.to_s + " notes file:"
    puts "(empty line to exit)"
    loop do
      tmp = gets.chomp.to_s
      break if tmp == ''
      file.puts tmp
    end
    file.puts '}'
  end

  def make_files(instrument)
    i = 1
    includes = File.new(@cd + '/' + instument.file + "_include.ily", "w")
    file_top(includes)
    includes.puts "#(ly:set-option 'relative-includes #t)"
    while i <= @movements.count
      file_name = instrument.file + '/' + instrument.file + '_' + i.to_s + '.ily'
      ins_file = File.new(@cd + '/' + file_name, "w")
      file_top(ins_file)
      put_var(ins_file)
      ins_file.close()
      includes.puts '\include "' + file_name + '"'
      i += 1
    end
  end

  def make_all()
    make_globals()
    @instruments.each do |ins|
      create(ins)
      make_files(ins)
    end
  end

  def initialize(info)
    @cd = Dir.pwd
    @instruments = info.instruments
    @version = info.version
    @movements = info.movements
    @language = info.language
  end

end

   
