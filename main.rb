#!/usr/bin/env ruby
#  main.rb - main function for lilypond-file-generator.

Dir[File.dirname(__FILE__) + '/classes/*.rb'].each { |file| require file }


info = Info.new
defs = Defs.new(info)
defs.create()
defs.write()
defs.done()
score = Score.new(info)
score.create()
score.write()
score.done()
for instrument in info.instruments
  part = Part.new(info, instrument)
  part.create()
  part.write()
  part.done()
end
structure = Directories.new(info)
structure.make_all()
