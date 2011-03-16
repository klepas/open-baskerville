# Todo: this uses posix specific path seperator ('/'),
# so it won’t work on Windows.

# Right now, OpenBaskerville.otf is regenerated when a file inside
# OpenBaskerville.ufo is changed.
# This should be: if the contents of *any* UFO folder changes,
# the *corresponding* otf should be regenerated. This allows for additional
# font styles, and for the reuse of this Rakefile across font projects.

# version = `python ./tools/version.py`

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
''rake''."
  end
end

# Check whether we are in the git repository
task :_has_git do
   unless File.directory? '.git'
     abort "This rake task needs to run inside a git working tree:
See http://openbaskerville.org/klepas on what git is and how to get it."
   end
end
