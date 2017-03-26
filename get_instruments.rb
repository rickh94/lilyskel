#!/usr/bin/env ruby
# get_includes.rb - Get the instruments the user wants in their Lilypond
# project.
#
# Large Chunks of this code will be revised by introduction of the Instrument
# Class.

class Instrument
  attr_reader :pretty, :file, :variable
  def initialize(input_name)
    @file = input
    # TODO: move some much of the name cleaning into the class.
    # TODO: figure out how to initialize classes and return to larger program later.
    # TODO: figure out how to programatically generate classes.
  end
end


def get_instruments()
  puts 'Please enter EACH instrument in the project separated by commas: '
  puts '(e.g. violin 1, violin 2, viola, etc.)'
  parts = gets.chomp.split(', ').map { |ins| ins.to_s.tr(' A-Z', '_a-z') }
  # normalize instruments list to instrument_name_[number]
  # supports up to ins_9, but have to be entered individually.
  # if you want more, enter them properly (preferably with leading zeros on
  # single digit numbers so they sort well.
  # NOTE: I wish this weren't so messy. I feel like there should be a more
  # efficient way to handle this but I can't seem to figure it out. sigh.
  # It does need to be VERY specific to avoid replacing random letters or
  # truncating whole words from instrument names. 
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
  end
  instrument_vars = parts.map { |ins| ins.gsub(/_[0-9]*$/,
                                               '_1' => '_one',
                                               '_2' => '_two',
                                               '_3' => '_three',
                                               '_4' => '_four',
                                               '_5' => '_five',
                                               '_6' => '_six',
                                               '_7' => '_seven',
                                               '_8' => '_eight',
                                               '_9' => '_nine'
                                              ) }
  return parts, instrument_vars
end

#things = get_instruments()
#print things.first
#print things.last

