#!/usr/bin/env ruby
# info_class.rb - class for gathering and storing all the needed info about a
# lilypond project (except includes which are handled elsewhere).

# Require statements for testing purposes only
require './instrument_class.rb'
require './headers_class.rb'
require './version_class.rb'

class Info
  attr_reader :instruments, :headers, :version, :language
  def get_instruments()
    # Get instruments from user
    puts 'Please enter each instrument in the project separated by commas: '
    puts '(e.g. violin 1, violin 2, viola, etc.)'
    parts = gets.chomp.split(',').map { |ins| ins.to_s.gsub(/^ /, '').tr(' A-Z', '_a-z') }

    # normalize instruments list to instrument_name_[number]
    # supports up to ins_9, but have to be entered individually.
    # if you want more, you have to edit the class. 
    parts.each do |ins| 
      # this replaces roman numberals
      ins.gsub!(/_[ivx]*$/,  
                '_i'    => '_1',
                '_ii'   => '_2',
                '_iii'  => '_3',
                '_iv'   => '_4',
                '_v'    => '_5',
                '_vi'   => '_6',
                '_vii'  => '_7',
                '_viii' => '_8',
                '_ix'   => '_9',
               )
      # this replaces number words with numbers
      ins.gsub!(/_one$/, '_1')
      ins.gsub!(/_two$/, '_2')
      ins.gsub!(/_three$/, '_3')
      ins.gsub!(/_four$/, '_4')
      ins.gsub!(/_five$/, '_5')
      ins.gsub!(/_six$/, '_6')
      ins.gsub!(/_seven$/, '_7')
      ins.gsub!(/_eight$/, '_8')
      ins.gsub!(/_nine$/, '_9')
      file_name = ins
      # Create new Instrument object for each instrument.
      file_name = Instrument.new(file_name.to_s)
    end
    #  Return array of all instruments (tracked internally by Instrument class.
    return Instrument.all_instances
  end

  def initialize()
    @version = Version.new.self
    @language = Language.new.self
    @instruments = get_instruments()
    @headers = Headers.new
  end
end

# TESTS for info
info = Info.new
puts info.version
puts info.language
puts info.headers.all()
info.instruments.each{ |i| puts i.pretty() }
