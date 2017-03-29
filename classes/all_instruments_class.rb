#!/usr/bin/env ruby 
#  all_instruments_class.rb - a class for getting instruments from 
#  user, normalizing their names and making an Instrument object for each.

#require './instrument_class.rb'
require File.dirname(__FILE__) + '/instrument_class.rb'

class AllInstruments
  @@input = Array.new
  @@all = Array.new

  def get_instruments()
    # Get instruments from user
    puts 'Please enter each instrument in the project separated by commas: '
    puts '(e.g. violin 1, violin 2, viola, etc.)'
    @@input = gets.chomp.split(',').map(&:lstrip)
  end

  def remove_spaces_and_caps()
    @@input.map{ |i| i.tr!(' A-Z', '_a-z') }
  end

  def normalize_roman_numerals()
    @@input.map{ |i| i.gsub!(/_[ivx]*$/,
                            '_i'    => '_1',
                            '_ii'   => '_2',
                            '_iii'  => '_3',
                            '_iv'   => '_4',
                            '_v'    => '_5',
                            '_vi'   => '_6',
                            '_vii'  => '_7',
                            '_viii' => '_8',
                            '_ix'   => '_9',
                           ) }
  end

  def normalize_number_words()
    @@input.each do |i|
      i.gsub!(/_one$/, '_1')
      i.gsub!(/_two$/, '_2')
      i.gsub!(/_three$/, '_3')
      i.gsub!(/_four$/, '_4')
      i.gsub!(/_five$/, '_5')
      i.gsub!(/_six$/, '_6')
      i.gsub!(/_seven$/, '_7')
      i.gsub!(/_eight$/, '_8')
      i.gsub!(/_nine$/, '_9')
    end
  end

  def create_instrument_objects()
    @@input.each do |i|
      tmp = i
      @@all << Instrument.new(tmp.to_s)
    end
  end


  def initialize()
    get_instruments()
    remove_spaces_and_caps()
    normalize_roman_numerals()
    normalize_number_words()
    create_instrument_objects()
  end

  def all()
    @@all
  end
end

# TESTS
#test = AllInstruments.new
#puts Instrument.all_instances
#puts test.all()
#test.all().each do |i|
  #puts i.file()
#end
