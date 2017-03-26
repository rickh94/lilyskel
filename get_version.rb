#!/usr/bin/env ruby
# get_version.rb - gets the version of lilypond currently installed and returns
# it.

def get_version()
  # Get Lilypond version by running lilypond from a shell.
  begin
    version = `lilypond --version`.scan(/\d\.\d+\.\d+/).first.to_s
  rescue
    # If Lilypond doesn't run, prompt user to check installation or enter
    # version number.
    puts "Could not run lilypond --version."
    puts "You can manually enter a version number, but you should check that " \
      "it is installed correctly"
    version = gets.chomp.to_s
  end
  # If Lilypond runs but no version number is found, prompt user
  if version == ''
    puts "Lilypond ran but could not find a version in output. Please enter it now:"
    version = gets.chomp.to_s
  end
  # Return version statement.
  '\\version "' + version + '"'
end

#puts getversion()
