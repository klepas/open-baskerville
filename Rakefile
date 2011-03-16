# Todo: this uses posix specific path seperator ('/'),
# so it won’t work on Windows.

# Right now, OpenBaskerville.otf is regenerated when a file inside
# OpenBaskerville.ufo is changed.
# This should be: if the contents of *any* UFO folder changes,
# the *corresponding* otf should be regenerated. This allows for additional
# font styles, and for the reuse of this Rakefile across font projects.

UFO = FileList.new('OpenBaskerville.ufo/**/*.*')

task :default => "OpenBaskerville.otf"

desc "Generate OpenType Font"
file 'OpenBaskerville.otf' => UFO do
  puts "Generating otf.."
  sh "python ./tools/ufo2otf.py OpenBaskerville.ufo OpenBaskerville.otf"
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
task :fontlog => :_has_git do
  sh "python ./tools/FONTLOG.py > FONTLOG.txt"
  puts "FONTLOG.txt generated"
end

# Check if there are otf files
task :_has_otf_files do
  if Dir["*.otf"].length == 0
    abort "No otf files found. You can generate a working copy by running
''rake''. You can build a release by running ''rake release''."
  end
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
task :_version_number => :_has_git do
  git_describe = `git describe`.strip
  # v0.0.0-49-gb5cc6c0 -> 0.0.49 (gb5cc6c0)
  # http://www.rubular.com/r/kqgRzxS8G9
  @version_number = git_describe.gsub /[v]?([0-9]+)\.([0-9]+)\.0-([0-9]+)-([\w]+)/  , '\1.\2.\3 (\4)'
  if @version_number == git_describe
    abort "Unable to automatically generate patch version number"
  end
  @version_number_short = @version_number.split[0]
  puts "Generated version number #{@version_number}"
end

task :_nokogiri do
  require 'nokogiri'
end

# Bake this version number into the UFO (and therefore, into generated OTF’s)
task :_bake_version_number => [:_version_number, :_nokogiri] do
# This would be cleaner to do with RoboFab, but Rakefiles need Ruby :)
  f = File.open("OpenBaskerville.ufo/fontinfo.plist","r")
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
  g = File.open("OpenBaskerville.ufo/fontinfo.plist","w")
  g.write(doc)
  g.close
  if success
    puts "Baked the generated version number into the UFO"
  else
    abort "Failed to bake the version number into the UFO"
  end
end

desc "Generate an OTF with proper version number in filename and metadata"
task :release => [:_head_clean, :_bake_version_number, :fontlog] do
  puts "Generating otf.."
  sh "python ./tools/ufo2otf.py OpenBaskerville.ufo OpenBaskerville-#{@version_number_short}.otf"
  puts "Built release #{@version_number_short}!"
end
