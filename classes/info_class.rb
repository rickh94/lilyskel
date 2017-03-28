#!/usr/bin/env ruby
# info_class.rb - class for gathering and storing all the needed info about a
# lilypond project (except includes which are handled elsewhere).

# Require statements for testing purposes only
#require './instrument_class.rb'
#require './headers_class.rb'
#require './version_class.rb'
#require './language_class.rb'
#require './version_class.rb'
#require './all_instruments_class.rb'

class Info
  attr_reader :instruments, :headers, :version, :language
  def initialize()
    @version = Version.new.self
    @language = Language.new.self
    @instruments = AllInstruments.new.all()
    @headers = Headers.new.all()
  end
end

# TESTS for info
#info = Info.new
#puts info.version
#puts info.language
#puts info.headers.all()
#info.instruments.each{ |i| puts i.pretty() }
