#!/usr/bin/env ruby
# directories.rb - Class for directory creation (and population).

class Directories

  # creates each directory
  def create(instrument)
    Dir.mkdir(@cd + '/' + instrument.file)
  end

  def make_files(instrument)
    i = 1
    while i <= movements.count
      file_prefix = @cd + '/' + instrument.file + '/' + instrument.file
      tmp = File.new(file_prefix + '_' + i + '.ily', "w")
      tmp.puts '\version "' + @version + '"'
      tmp.puts '\language "' + @language + '"'
      tmp.puts "\n\n\n\\" + @instrument.var + '_' + @movements.movement_number(i) \
        + ' = \relative {'
      tmp.puts '}'
      tmp.close()
      i += 1
    end
  end

  def all()
    @instruments.all.each do |i|
      create(i)
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

   
