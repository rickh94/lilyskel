#!/usr/bin/env ruby
#  output_classes.rb - classes for creation of files: Output and subclasses
#  Score and Part. Generate and write files given inputs.


class Part < Output
  # change initialize
  def initialize(info, instrument)
    @vers = info.version
    @lang = info.language
    @heads = info.headers
    @instr = instrument # this is an instrument object, not just a name.
  end

  def filename()
    filename_prefix() + '_' + @instr.file() + '.ly'
  end

  def name()
    @instr.pretty()
  end
end

# TESTS for the Part Class
#tests = { "opus" => "Op. 15", "title" => "Test Title"}
#tests_2 = { "title" => "Test Title" }
#vio = Instrument.new("violin_1")
#part = Part.new("vers", "lang", tests, vio)
#part.create()
#part.write()
#part.done()
