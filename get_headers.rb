#!/usr/bin/env ruby
# get_headers.rb - Gets all header info from user and outputs a hash
# containing appropriate key value pairs.

def get_headers()
  # Get normal header information from user.
  header = Hash.new
  puts "Please enter the composer of the piece: "
  header['composer'] = gets.chomp.to_s
  puts "Please enter the title of the piece: "
  header['title'] = gets.chomp.to_s
  puts "Please enter the subtitle: (blank for none)"
  header['subtitle'] = gets.chomp.to_s
  puts "Please enter the arranger: (blank for none)"
  header['arranger'] = gets.chomp.to_s
  puts "Please enter the opus of the piece: (blank for none)"
  header['opus'] = gets.chomp.to_s
  puts "Please enter the copyright information of the piece: (blank for none)"
  header['copyright'] = gets.chomp.to_s

  # Get Mutopia headers if applicable.
  print "Will this piece be submitted to the Mutopia Project? [y/N]"
  if gets.chomp.to_s.downcase.split('').first == "y"
    puts "Enter mutopia title if different: "
    header['mutopiatitle'] = gets.chomp.to_s
    puts "Enter mutopiacomposer in the form surnameINITIALS (e.g. BachJS):"
    header['mutopiacomposer'] = gets.chomp.to_s
    puts "Enter mutopia opus if different: "
    header['mutopiaopus'] = gets.chomp.to_s
    puts "Enter date piece was composed: (blank for none)"
    header['date'] = gets.chomp.to_s
    puts "Please select the license you would like to release under:"
    puts "1. Creative Commons Attribution-ShareAlike 4.0"
    puts "2. Creative Commons Attribution 4.0"
    puts "3. Public Domain"
    answer = gets.chomp.to_s.split('').first
    if answer == "1"
      header['license'] = "Creative Commons Attribution-ShareAlike 4.0"
    elsif answer == "2"
      header['license'] = "Creative Commons Attribution 4.0"
    else
      header['license'] = "Public Domain"
    end # of license selector
    puts "Enter your name for the maintainer field: "
    maintainer = gets.chomp.to_s
    maintainer == '' ? header['maintainer'] = 'Anonymous' : header['maintainer'] = maintainer
    puts "Enter your email (optional): "
    header['maintainerEmail'] = gets.chomp
  end # of mutopia headers

  #  Return array of only the populated header fields. This way empty header
  #  fields won't be explicit and can be changed, overwritten, or overridden
  #  easily.
  header.reject{|k, v| v == '' }
end

#print get_headers()
