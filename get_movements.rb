#!/usr/bin/env ruby
# get_movements.rb - Get the Number of instruments and return array of ordinal
# movement numbers for use in note variables. Supports up to twelve movements.
#
# TODO: create movements class that will output movement count, any of the
# movement words, or all of them.

def get_movements()
  # Array of ordinal_mov for use in instrument note variables
  ordinal_movements = ['first_mov', 'second_mov', 'third_mov', 'fourth_mov', 
                       'fifth_mov', 'sixth_mov', 'seventh_mov', 'eighth_mov',
                       'ninth_mov', 'tenth_mov', 'eleventh_mov', 'twelfth_mov']

  # Get number of movements from user
  print 'Please enter the number of movements for the project: '
  movements = gets.chomp.to_i

  # return array of movement words
  ordinal_movements.take(movements)
end

#things = get_movements()
#things.each { |x| print x + "\n" }
