#!/usr/bin/env ruby
# language_class.rb - Gets user to select language. Converts into language and
# will pass it to info class.

class Language
  attr_reader :self
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
    # Force choice of language.
    loop do
      puts "=== Languages Supported by Lilypond ==="
      supported_languages.each { |k, v| puts k + '. ' + v }
      print "Please enter the number of the language you would like to use in Lilypond: "
      input = gets.chomp.to_s
      # Filter out mistaken or out of range input
      if input.to_i <= 13 && input.to_i > 0 && input.to_s != '' 
        num = input.to_s.rjust(2, "0")
        supported_languages.each { |k, v| num.to_s.gsub!(k.rjust(2, "0"), v) }
        return num
      else
        puts 'Number entered is out of range. Please try again'
      end
    end
  end

  def initialize()
    @self = get_language()
  end
end
