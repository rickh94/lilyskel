#!/usr/bin/env ruby
#  output_classes.rb - classes for creation of files: Output and subclasses
#  Score and Part. Generate and write files given inputs.

#require File.dirname(__FILE__) + '/output_class.rb'

class Score < Output
  # Filename generation for Score.
  def filename()
    #  Make the score filename
    filename_prefix() + '_score.ly'
  end

  def write_above(num)
    @file.puts '  % ' + @movs.comment(num)
    @file.puts '  \score {'
    @file.puts '   <<'
  end

  def write_mov(num)
    @instrs.each_with_index do |ins, i| 
      mov = @movs.movement_number(num)
      @file.puts '    \new Staff = "' + i.file + '" {'
      @file.puts '      \new Voice {'
      if i == 0
        @file.puts '      <<'
        @file.puts '        \global_' + mov
      end
      @file.puts "        \\" + ins.var + '_' + mov
      @file.puts '       >>' if i == 0
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
      write_above(i)
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
#info = Info.new
#score = Score.new(info)
#score.create()
#score.write()
#score.done()
