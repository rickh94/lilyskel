#!/usr/bin/env ruby
# getversion.rb - gets the version of lilypond currently installed and returns
# it.

def getversion()
  begin
    version = `lilypond --version`.scan(/\d\.\d+\.\d+/).first.to_s
  rescue
    puts "Could not run lilypond --version."
    puts "You can manually enter a version number, but you should check that " \
      "it is installed correctly"
    version = gets.chomp.to_s
  end
  unless version == ''
    version
  else
    puts "Lilypond ran but could not find a version in output. Please enter it now"
    version = gets.chomp.to_s
  end
end

puts getversion()
