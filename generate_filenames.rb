#!/usr/bin/env ruby
# generate_filenames.rb - combines the headers and instruments to return an
# array of filenames that need to be created.

require './get_headers.rb'
require './get_instruments.rb'

def generate_filenames(headers, instruments)
  #  Array to hold all needed filenames.
  filenames = Array.new

  #  If there is an opus, use that for the filename prefix, otherwise use the
  #  title.
  headers.has_key?("opus") ? 
    prefix = headers['opus'].gsub('Op. ', 'O').tr(' ', '_').upcase :
    prefix = headers['title'].downcase.tr(' ', '_').gsub('.', '')

  #  Make the score filename
  score_name = Array.new
  score_name << prefix
  score_name << '_score'
  score_name << '.ly'
  filenames << score_name.join('')

  #  Make filenames for each instrument.
  instruments.each do |ins|
    tmp = Array.new
    tmp << prefix
    tmp << '_' + ins.file.to_s
    tmp << '.ly'
    filenames << tmp.join('')
  end # of instrument filename creator

  # return filenames in array
  filenames
end

#head = get_headers()
#ins = get_instruments()
#puts generate_filenames(head, ins)
