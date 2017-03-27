#!/usr/bin/env ruby
# get_includes.rb - Get the dependency files the user wants to include with
# their lilypond project.

def get_includes()
  # get names of include files
  puts 'Please enter the file names you would like to include '\
    'in your Lilypond project, separated by commas:'
  files = gets.chomp.to_s.split(', ')

  # Generate individual include statments
  includes = Array.new
  files.each do |file|
    includes << '\\include "' + file.to_s + '"'
  end
  # Return array of include statements
  includes
end

#things = get_includes()
#things.each { |x| print x + "\n" }
