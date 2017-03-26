#!/usr/bin/env ruby
# get_movements.rb - Get the Number of instruments and return array of ordinal
# movement numbers for use in note variables. Supports up to twelve movements.

def get_movements()
  ordinal_movements = ['first_mov', 'second_mov', 'third_mov', 'fourth_mov', 
                       'fifth_mov', 'sixth_mov', 'seventh_mov', 'eighth_mov',
                       'ninth_mov', 'tenth_mov', 'eleventh_mov', 'twelfth_mov']
  print 'Please enter the number of movements for the project: '
  movements = gets.chomp.to_i
  ordinal_movements.take(movements)
end

#things = get_movements()
#things.each { |x| print x + "\n" }
