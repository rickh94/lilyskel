#!/usr/bin/env ruby
#  output_classes.rb - classes for creation of files: Output and subclasses
#  Score and Part. Generate and write files given inputs.

#require './output_class.rb'


class Part < Output
  # change initialize
  def initialize(info, instrument)
    @vers = info.version
    @lang = info.language
    @heads = info.headers
    @instr = instrument # this is an instrument object, not just a name.
    @movs = info.movements
  end

  def filename()
    filename_prefix() + '_' + @instr.file() + '.ly'
  end

  def write_above(num)
    @file.puts '  % ' + @movs.comment(num)
    @file.puts '  \score {'
    @file.puts '    \new Staff {'
    @file.puts '      \new Voice {'
    @file.puts '       <<'
  end

  def write_mov(num)
    mov = @movs.movement_number(num)
    @file.puts "      \global_" + mov
    @file.puts "      \\" + @instr.var + '_' + mov
  end

  def write_below()
    @file.puts '       >>'
    @file.puts '      }'
    @file.puts '    }'
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
    @instr.pretty
  end
end

# TEST for the Part Class
=begin
info = Info.new
info.instruments.each do |ins|
  part = Part.new(info, ins)
  part.create()
  part.write()
  part.done()
end
=end
