#!/usr/bin/env ruby
# headers_class.rb - class for collecting and holding Header information in a
# hash.

class Headers
  attr_reader :all
  @@all = Hash.new
  def get_composer()
    # force input of composer
    loop do
      puts "Please enter the composer of the piece: "
      @@all['composer'] = gets.chomp.to_s
      break if @@all['composer'] != '' 
    end
  end

  def get_title()
    # force input of title
    loop do
      puts "Please enter the title of the piece: "
      @@all['title'] = gets.chomp.to_s
      break if @@all['title'] != '' 
    end
  end

  def get_subtitle()
    puts "Please enter the subtitle: (blank for none)"
    @@all['subtitle'] = gets.chomp.to_s
  end

  def get_arranger()
    puts "Please enter the arranger: (blank for none)"
    @@all['arranger'] = gets.chomp.to_s
  end

  def get_opus()
    puts "Please enter the opus of the piece: (blank for none)"
    @@all['opus'] = gets.chomp.to_s
  end

  def get_copyright()
    puts "Please enter the copyright information of the piece: (blank for none)"
    @@all['copyright'] = gets.chomp.to_s
  end

  def mutopia_title()
    puts "Enter mutopia title if different: "
    @@all['mutopiatitle'] = gets.chomp.to_s
  end

  def mutopia_composer()
    puts "Enter mutopiacomposer in the form surnameINITIALS (e.g. BachJS):"
    @@all['mutopiacomposer'] = gets.chomp.to_s
  end

  def mutopia_opus()
    puts "Enter mutopia opus if different: "
    @@all['mutopiaopus'] = gets.chomp.to_s
  end

  def mutopia_date()
    puts "Enter date piece was composed: (blank for none)"
    @@all['date'] = gets.chomp.to_s
  end

  def license_select()
    puts "Please select the license you would like to release under:"
    puts "1. Creative Commons Attribution-ShareAlike 4.0"
    puts "2. Creative Commons Attribution 4.0"
    puts "3. Public Domain (default)"
    answer = gets.chomp.to_s.split('').first
    if answer == "1"
      @@all['license'] = "Creative Commons Attribution-ShareAlike 4.0"
    elsif answer == "2"
      @@all['license'] = "Creative Commons Attribution 4.0"
    else
      @@all['license'] = "Public Domain"
    end 
  end

  def mutopia_mainatainer()
    puts "Enter your name for the maintainer field: "
    maintainer = gets.chomp.to_s
    maintainer == '' ? @@all['maintainer'] = 'Anonymous' : @@all['maintainer'] = maintainer
  end

  def mutopia_email()
    puts "Enter your email (optional): "
    @@all['maintainerEmail'] = gets.chomp
  end

  def get_mutopia()
    print "Will this piece be submitted to the Mutopia Project? [y/N]"
    return if gets.chomp.to_s.downcase.split('').first != 'y'
    mutopia_title()
    mutopia_composer()
    mutopia_opus()
    mutopia_date()
    license_select()
    mutopia_mainatainer()
    mutopia_email()
  end

  def get_all()
    get_composer()
    get_title()
    get_subtitle()
    get_arranger()
    get_opus()
    get_copyright()
    get_mutopia()
  end
  
  def initialize()
    get_all()
  end

  def all()
    @@all.reject{|k, v| v == '' }
  end
end

# TESTS
#heads = Headers.new

#puts "\ncurrent headers"
#heads.all().each { |k, v| puts k.to_s + ' = ' + v.to_s }

# TODO: get this later for defs or info class. Complicate it to implement
# it here.
=begin
      tmp = Array.new
      instruments.each { |ins| tmp << ins.pretty }
      header['mutopiainstrument'] = tmp.join(', ').gsub(/(Violon)?[cC]ello/, "'Cello")
=end
