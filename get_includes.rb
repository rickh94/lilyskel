#!/usr/bin/env ruby
# get_includes.rb - Get the language the user intends to input notes with and 
# output a langauge statement for lilypond.

def get_includes()
  puts 'Please enter the file names you would like to include '\
    'in your Lilypond project, separated by spaces:'
  files = gets.chomp.to_s.split(' ')
  includes = Array.new
  files.each do |file|
    includes << '\\include "' + file.to_s + '"'
  end
  includes
end

#things = get_includes()
#things.each { |x| print x + "\n" }
