#!/usr/bin/env ruby
# instrument_class.rb - defines Instrument Class for storing/generating all needed information

class Instrument
  @@array = Array.new
  attr_reader :file, :var, :pretty
  # array to keep track of all Instruments internally
  def self.all_instances
    @@array
  end


  # method to generate word version of name for use in instrument variables
  def make_variable()
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
  def make_pretty()
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

  def initialize(input_name)
    @file = input_name.to_s
    @@array << self
    @var = make_variable()
    @pretty = make_pretty()
  end
end
