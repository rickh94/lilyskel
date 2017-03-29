#!/usr/bin/env ruby
# movements_class.rb - Get the number of movements. Give access to movement
# words for variables and a count of the movements.

class Movements
  attr_reader :count
  @@ordinal_movements = ['first_mov', 'second_mov', 'third_mov', 'fourth_mov', 
                       'fifth_mov', 'sixth_mov', 'seventh_mov', 'eighth_mov',
                       'ninth_mov', 'tenth_mov', 'eleventh_mov', 'twelfth_mov']

  @@number_words = ['First Movement', 'Second Movement', 'Third Movement', 'Fourth Movement',
                    'Fifth Movement', 'Sixth Movement', 'Seventh Movement', 'Eighth Movement',
                    'Ninth Movement', 'Tenth Movement', 'Eleventh Movement', 'Twelfth Movement']
  def initialize()
    puts "How many movements are in the piece?"
    @count = gets.chomp.to_i
  end

  def movement_number(num)
    if num <= @count
      @@ordinal_movements[num - 1]
    else
      # This should not really be needed but is useful for debugging purposes.
      # Plus it's good practice not to allow things that shouldn't exist.
      abort("Exception: Out of Range: Tried to generate move movements than are in the piece.")
    end
  end

  def comment(num)
    if num <= @count
      @@number_words[num - 1]
    else
      abort("Exception: Out of Range: Tried to generate move movements than are in the piece.")
    end
  end
end

#TESTS
#test = Movements.new
#puts test.movement_number(5)
