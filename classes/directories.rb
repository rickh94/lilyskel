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

  def make_files(instrument)
    i = 1
    while i <= @movements.count
      file_prefix = @cd + '/' + instrument.file + '/' + instrument.file
      ins_file = File.new(file_prefix + '_' + i.to_s + '.ily', "w")
      ins_file.puts '\version "' + @version + '"'
      ins_file.puts '\language "' + @language + '"'
      puts "Please enter additional text for the top secion of " + instrument.pretty + " notes files:"
      puts "(empty line to exit)"
      loop do
        tmp = gets.chomp.to_s
        break if tmp == ''
        ins_file.puts tmp
      end
      ins_file.puts "\n\n\n" + instrument.var + '_' + @movements.movement_number(i) \
        + ' = \relative {'
      puts "Please enter additional text for the variable secion of " + instrument.pretty + " notes files:"
      puts "(empty line to exit)"
      loop do
        tmp = gets.chomp.to_s
        break if tmp == ''
        ins_file.puts tmp
      end
      ins_file.puts '}'
      ins_file.close()
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

   
