#!/usr/bin/env ruby
# get_language.rb - Get the language the user intends to input notes with and 
# output a langauge statement for lilypond.

def get_language()
  # Array of supported languages from Lilypond documentation.
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
  # Ask for input language, keep asking until valid language is entered.
  language = String.new
  loop do
    puts "Please enter the language you would like to use for you lilypond input:"
    language = gets.chomp.to_s.downcase
    if supported_languages.include?(language)
      # If language is suppported you're done!
      break
    else
      # If language is unsupported list supported languages and try again.
      puts "\nThat language is not supported by Lilypond."
      puts "=== Languages Supported by Lilypond ==="
      supported_languages.each_slice(2) { |lang1, lang2| 
        puts ''.ljust(5) + lang1.to_s.ljust(14) + '   ' + lang2.to_s 
      }
      puts ''
    end
  end
  # return language statement
  '\\language "' + language + '"'
end

#puts getlanguage()
