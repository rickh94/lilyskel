#!/usr/bin/env ruby
# getlanguage.rb - Get the language the user intends to input notes with and 
# output a langauge statement for lilypond.

def getlanguage()
  supported_languages = [
    "nederlands",
    "catalan",
    "deutsch",
    "english",
    "espanol",
    "español",
    "italiano",
    "français",
    "norsk",
    "portugues",
    "suomi",
    "svenska",
    "vlaams"
  ]
  language = String.new
  loop do
    puts "Please enter the language you would like to use for you lilypond input:"
    language = gets.chomp.to_s.downcase
    if supported_languages.include?(language)
      break
    else
      puts "\nThat language is not supported by Lilypond."
      puts "=== Languages Supported by Lilypond ==="
      supported_languages.each_slice(2) { |lang1, lang2| 
        puts ''.ljust(5) + lang1.to_s.ljust(14) + '   ' + lang2.to_s 
      }
      puts ''
    end
  end
  '\\language "' + language + '"'
end

#puts getlanguage()
