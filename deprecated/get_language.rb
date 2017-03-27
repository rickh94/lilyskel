#!/usr/bin/env ruby
# get_language.rb - Get the language the user intends to input notes with and 
# output a langauge statement for lilypond.

def get_language()
  # Array of supported languages from Lilypond documentation.
  supported_languages = {
    "1"  => "nederlands",
    "2"  => "catalan",
    "3"  => "deutsch",
    "4"  => "english",
    "5"  => "espanol",
    "6"  => "español",
    "7"  => "italiano",
    "8"  => "français",
    "9"  => "norsk",
    "10" => "portugues",
    "11" => "suomi",
    "12" => "svenska",
    "13" => "vlaams"
  }
  loop do
    puts "Please enter the number of the language you would like to use in lilypond"
    puts "=== Languages Supported by Lilypond ==="
    supported_languages.each { |k, v| puts k + '. ' + v }
    input = gets.chomp.to_s
    if input.to_i <= 13 && input.to_i > 0 && input.to_s != '' 
      num = input.to_s.rjust(2, "0")
      supported_languages.each { |k, v| num.to_s.gsub!(k.rjust(2, "0"), v) }
      return num
    else
      puts 'Number entered is out of range. Please try again'
    end
  end
end
  ## Ask for input language, keep asking until valid language is entered.
  #  language = String.new
  #  puts "Please enter the language you would like to use for you lilypond input:"
  #  language = gets.chomp.to_s.downcase
  #  if supported_languages.include?(language)
  #    # If language is suppported you're done!
  #    break
  #  else
  #    # If language is unsupported list supported languages and try again.
  #    puts "\nThat language is not supported by Lilypond."
  #    supported_languages.each_slice(2) { |lang1, lang2|
  #      puts ''.ljust(5) + lang1.to_s.ljust(14) + '   ' + lang2.to_s
  #    }
  #    puts ''
  #  end
  #end
  ## return language statement
  #'\\language "' + language + '"'
#end
lang = get_language()
puts lang

#puts getlanguage()
