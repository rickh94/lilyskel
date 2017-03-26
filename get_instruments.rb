#!/usr/bin/env ruby
# get_includes.rb - Get the instruments the user wants in their Lilypond
# project. Return array of Instrument objects that can generate needed
# information.

class Instrument
  @@array = Array.new
  attr_reader :file

  # array to keep track of all Instruments internally
  def self.all_instances
    @@array
  end

  def initialize(input_name)
    @file = input_name.to_s
    @@array << self
  end

  # method to generate word version of name for use in instrument variables
  def variable()
    @file.to_s.gsub(/_[0-9]*$/,
                 '_1' => '_one',
                 '_2' => '_two',
                 '_3' => '_three',
                 '_4' => '_four',
                 '_5' => '_five',
                 '_6' => '_six',
                 '_7' => '_seven',
                 '_8' => '_eight',
                 '_9' => '_nine'
                )
  end

  # Method to generate pretty version of instrument name for printing
  def pretty()
    @file.split('_').map(&:capitalize).join(' ').gsub(/ [0-9]*$/, 
                                                         ' 1' => ' I', 
                                                         ' 2' => ' II',
                                                         ' 3' => ' III',
                                                         ' 4' => ' IV',
                                                         ' 5' => ' V',
                                                         ' 6' => ' VI',
                                                         ' 7' => ' VII',
                                                         ' 8' => ' VIII',
                                                         ' 9' => ' IX' )
  end
end


def get_instruments()

  # Get instruments from user
  puts 'Please enter EACH instrument in the project separated by commas: '
  puts '(e.g. violin 1, violin 2, viola, etc.)'
  parts = gets.chomp.split(', ').map { |ins| ins.to_s.tr(' A-Z', '_a-z') }

  # normalize instruments list to instrument_name_[number]
  # supports up to ins_9, but have to be entered individually.
  # if you want more, you have to edit several scripts. It's probably faster
  # to copy existing files and edit stuff manually.
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

#things = get_instruments()
#things.each do |x|
#  print x.file.to_s + ' ' + x.pretty.to_s + ' ' + x.variable.to_s  + "\n"
#end
#print things.last
