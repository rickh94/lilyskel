#!/usr/bin/env ruby
#  output_classes.rb - classes for creation of files: Output and subclasses
#  Score and Part. Generate and write files given inputs.

require './output_class.rb'

class Score < Output
  # Filename generation for Score.
  def filename()
    #  Make the score filename
    filename_prefix() + '_score.ly'
  end

  def write_above()
    @file.puts '  \score {'
    @file.puts '   <<'
  end

  def write_mov(num)
    for i in @instrs
      @file.puts '    \new Staff = "' + i.file + '" {'
      @file.puts '      \new Voice {'
      @file.puts "        \\" + i.var + '_' + @movs.movement_number(num)
      @file.puts '      }'
      @file.puts '    }'
    end
  end

  def write_below()
    @file.puts '   >>'
    @file.puts '  }'
  end

  def write_middle()
    i = 1
    while i <= @movs.count 
      write_above()
      write_mov(i)
      write_below()
      i += 1
    end
  end

  def name()
    "Score"
  end
end

# TESTS for the Score Class
info = Info.new
score = Score.new(info)
score.create()
score.write()
score.done()
