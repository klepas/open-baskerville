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
task :install => "OpenBaskerville.otf" do
  if  RUBY_PLATFORM.include? 'darwin'
    sh "cp *.otf ~/Library/Fonts/"
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