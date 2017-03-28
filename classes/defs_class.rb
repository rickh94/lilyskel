#!/usr/bin/env ruby
#  defs_class.rb - classes for creation of defs.ily file.

# Defs sublcass of output
class Defs < Output
  # change initialize
  def initialize(info)
    @vers = info.version
    @lang = info.language
    @heads = info.headers
    puts 'Please enter the file names you would like to include'\
      'in your Lilypond project, separated by commas:'
    @includes = gets.chomp.to_s.split(',').map(&:lstrip)
    @insts = info.instruments
  end

  def filename()
    'defs.ily'
  end

  def write_supporting()
    @file.puts "\n" + '\header {'
    @heads.each { |k, v| @file.puts '  ' + k + ' = "' + v + '"' }
    if @heads.has_key?('mutopiacomposer')
      tmp = Array.new
      @insts.each{ |i| tmp << i.pretty }
      @file.puts 'mutopiainstrument = "' + \
        tmp.join(', ').gsub(/(Violon)?[cC]ello/, "'Cello") + '"'
    end
    @file.puts '}'
  end

  def write_middle()
    @file.puts "\n\n#(ly:set-option 'relative-includes #t)"
    @includes.each { |i| @file.puts '\include "' + i + '"' }
  end

  def write_bottom()
    # this type doesn't have a different closing thing
  end
end

# TESTS for the Defs Class
#tests = { "opus" => "Op. 15", "title" => "Test Title"}
#defs = Defs.new("vers", "lang", tests)
#defs.create()
#defs.write()
#defs.done()
