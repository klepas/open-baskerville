# encoding: utf-8
# Rakefile for Font Development
# Eric Schrijver
# Requires Git > 1.7.0 and FontForge-Python
#
# This won’t work on Windows: it uses quite a lot of unix utilities.

def shortest_prefix(items)
  # Shortest prefix shared by an array of strings
  # http://www.ruby-forum.com/topic/120401#538016
  s = []
  a ,b = items.max.split(//), items.min.split(//)
  a.each_with_index{|x,y|s << y if x != b[y]}
  s.empty? ? a.join() : a[0...s[0]].join()
end

def args(items)
  # Join a list of filenames for use as command line arguments
  '"' + items.join('" "') + '"'
end

@ufos = Dir.glob('*.ufo')
# Todo: like this we find only the UFO’s that are in the root-folder.
# It’s better to recursively find all UFO’s in subfolders as well.
# When implementing this we should make sure all the other tasks
# are robust enough to handle various kinds of paths.

# Normally, the Rakefile should automatically figure out a common fileslug
# to use for your zipfiles etcetera, based on the common prefix of your UFO’s.
# (see rake task: :_get_slug)
# Alternatively, manually specify here:
@project_slug = ""

task :default => :otf

desc "Generate OpenType Fonts"
task :otf => :_has_ufos do
  puts "Generating otf.."
  sh "python ./tools/ufo2otf.py #{args @ufos}"
  puts "Done!"
# This is not extremely efficient, since the otf is going to be created
# regardless of whether the UFO has changed or not.
# I used to check for a filelist like this:
# file 'OpenBaskerville.otf' => FileList.new('OpenBaskerville.ufo/**/*.*') do
#   etc
# end
# Do you think it is worth the hassle to recreate that for *.ufo?
end

desc "Generate webfonts"
# For the instant, due to how ufo2otf is constructed,
# this will also generate the otf’s
task :webfonts => :_has_ufos do
  puts "Generating otf & webfonts.."
  sh "python ./tools/ufo2otf.py --webfonts #{args @ufos}"
  puts "Done!"
end

desc "Install OpenType Fonts"
task :install => :_has_otf_files do
  if  RUBY_PLATFORM.include? 'darwin'
    sh "cp *.otf ~/Library/Fonts/"
    puts "installed"
  else
    puts "Not implemented yet for this platform.
Please contribute patches!
You can consult for details on where to install fonts:
http://fontforge.sourceforge.net/faq.html#font-install"
  end
end

desc "Diagnose font build environment"
task :diagnostics do
  sh 'python ./tools/ufo2otf/diagnostics.py'
end

desc "Generate a FONTLOG.txt"
task :fontlog => :_build_folder do
  sh "python ./tools/FONTLOG.py > #{@build_folder}/FONTLOG.txt"
  puts "FONTLOG.txt generated"
end

desc "Start keeping track of version numbers"
task :init do
  git_describe = `git describe`.strip
  if $?.to_i == 0 and git_describe =~ /[v]?([0-9]+)\.([0-9]+)/
    abort "A valid version number tag has already been found."
  end
  puts "No suitable version tags found. We will add the first one. You can enter the version number from which to start font development:"
  Rake::Task["_version_number:init"].invoke
end

# Check if there are ufo files
task :_has_ufos do
  if @ufos.empty?
    abort "No UFO’s were found in the project root folder! This Rakefile is designed to work with UFO font files."
  end
end

# Check if there are otf files
task :_has_otf_files do
  if Dir["*.otf"].length == 0
    abort "No otf files found. You can generate a working copy by running
''rake''. You can build a release by running ''rake release''."
  end
end

# Make the build folder
task :_build_folder => :_version_number do
  @ufos.each do |ufo|
    release_ufo = ufo.sub('.ufo', '-' + @version_number_short + '.ufo')
    @build_folder = 'build/' + @release_slug
    sh "mkdir -p #{@build_folder}"
    sh "cp -r #{ufo} #{@build_folder}/#{release_ufo}"
  end
end

# Determine the project file slug
task :_get_slug => :_has_ufos do
  # This will take the prefix all your UFO’s have in common as the project slug
  # (Which is the name for the zip archive etc.)
  # Unless another slug is already specified in the top of the Rakefile
  if @project_slug == ""
    @project_slug = shortest_prefix(@ufos).sub(' ','_').sub('.ufo','')
  end
  if @project_slug == ""
    abort "No project file slug could be determined automatically.
Please specify in top of the Rakefile."
  end
  puts "Project slug is: #{@project_slug}"
end

# Check whether we are in the git repository
task :_has_git do
   unless File.directory? '.git'
     abort "This rake task needs to run inside a git working tree:
See http://openbaskerville.org/klepas on what git is and how to get it."
   end
end

# Check if the HEAD is clean
task :_head_clean => :_has_git do
  # This only works if Git >= 1.7.0
  if `git status --porcelain` != ""
    abort "You can only build releases from a clean working tree"
  else
    puts "HEAD clean"
  end
end

# Derive a version number from the current tag + number of commits (patch
# version)
task :_version_number => [:_has_git, :_get_slug] do
  git_describe = `git describe`.strip
  if $?.to_i != 0
    abort "Couldn’t find any version number tags! This script uses the built in tag functionality of the Git versioning system as the basis for generating version numbers. Consider adding version numbers with 'rake init'"
  end
  if git_describe =~ /[v]?([0-9]+)\.([0-9]+)\.0-([0-9]+)-([\w]+)/
    @major_version = $1
    @minor_version = $2
    @version_number = "#{$1}.#{$2}.#{$3} (#{$4})"
    @version_number_short = "#{$1}.#{$2}.#{$3}"
  elsif git_describe =~ /[v]?([0-9]+)\.([0-9]+)/
    @major_version = $1
    @minor_version = $2
    @version_number = @version_number_short = "#{$1}.#{$2}"
  else
    abort "Couldn’t parse version number from git tags. Consider (re-)initialising the version number with 'rake init'"
  end
  @release_slug = @project_slug + '-' + @version_number_short
  puts "Generated version number #{@version_number}"
  puts "Release slug: #{@release_slug}"
end

namespace :_version_number do
  task :init do
    puts "Major version number? (leave empty for 0, default)"
    major = $stdin.gets.to_i
    # btw, this relies on "\n".to_i returning 0
    puts "Minor version number? (leave empty for 0, default)"
    minor = $stdin.gets.to_i
    sh "git tag -a #{major}.#{minor} -m 'Start keeping track of version numbers programmatically'"
  end
end 

desc "Bump the major version number (i.e. 0.6 -> 1.0)"
task :major_bump =>  :_version_number do
    @major_version = @major_version.to_i + 1
    @minor_version = 0
    @version_number_short = "#{@major_version}.#{@minor_version}"
    puts "Bump version to #{@version_number_short}"
    sh "git tag -a #{@version_number_short} -m 'Programmatically bumped major version number to #{@version_number_short}'"
end

desc "Bump the minor version number (i.e. 0.6 -> 1.0)"
task :minor_bump =>  :_version_number do
    @minor_version = @minor_version.to_i + 1
    @version_number_short = "#{@major_version}.#{@minor_version}"
    puts "Bump version to #{@version_number_short}"
    sh "git tag -a #{@version_number_short} -m 'Programmatically bumped minor version number to #{@version_number_short}'"
end

task :_nokogiri do
  require 'nokogiri'
end

# Bake this version number into the UFO (and therefore, into generated OTF’s)
task :_bake_version_number => [:_build_folder, :_nokogiri] do
# This would be cleaner to do with RoboFab, but Rakefiles need Ruby :)
  release_ufos = Dir.glob("#{@build_folder}/*.ufo")
  release_ufos.each do |release_ufo|
    f = File.open("#{release_ufo}/fontinfo.plist","r")
    doc = Nokogiri::XML(f)
    f.close
    keys = doc.css("dict key")
    success = false
    keys.each do |node|
      if node.content == "openTypeNameVersion"
        node.next_element.content = @version_number
        success = true
      elsif  ["familyName","macintoshFONDName","postscriptFullName", "styleMapFamilyName"].include?(node.content)
        node.next_element.content += ' ' + @version_number_short
      elsif node.content == "postscriptFontName"
        #No spaces in postscriptFontName
        node.next_element.content += @version_number_short
      end
    end
    g = File.open("#{release_ufo}/fontinfo.plist","w")
    g.write(doc)
    g.close
    if success
      puts "Baked the generated version number into #{release_ufo}"
    else
      abort "Failed to bake the version number into #{release_ufo}"
    end
  end
end

# copy various other files intended for the package
task :_bundle_for_release => :_build_folder do
  # this should be with a file list defined in the top of the file
  sh "cp *.txt #{@build_folder}/"
end

desc "Generate an OTF with proper version number in filename and metadata"
task :release => [:_head_clean, :_bake_version_number, :fontlog, :_bundle_for_release] do
  release_ufos = Dir.glob("#{@build_folder}/*.ufo")
  puts "Generating otf.."
  sh "python ./tools/ufo2otf.py #{args release_ufos} --webfonts"
  puts "Built release #{@version_number_short}!"
end

desc "Generate a zip"
task :package => :release do
  sh "zip -r #{@release_slug}.zip #{@build_folder}"
  puts "generated #{@release_slug}.zip"
end

