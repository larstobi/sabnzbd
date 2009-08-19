#!/usr/bin/env python

Win32ConsoleName = 'SABnzbd-console.exe'
Win32WindowName  = 'SABnzbd.exe'

import sabnzbd
from distutils.core import setup

# py2exe usage: python setup.py py2exe

try:
    import glob
    import sys
    import os
    import py2exe
except ImportError:
    py2exe = None

print sys.argv[0]

if (len(sys.argv) < 2) or sys.argv[1] != 'py2exe':
    py2exe = None

options = dict(
      name = 'SABnzbd',
      version = sabnzbd.__version__,
      url = 'http://sourceforge.net/projects/sabnzbdplus',
      author = 'The ShyPike & Gregor Kaufmann',
      author_email = 'shypike@users.sourceforge.net',
      description = 'SABnzbd ' + str(sabnzbd.__version__),
      scripts = ['SABnzbd.py'],
      packages = ['sabnzbd', 'sabnzbd.utils', 'sabnzbd.utils.multiauth'],
      platforms = ['posix'],
      license = 'GNU General Public License 2 (GPL2)',
      data_files = [
          ('interfaces/Default/templates', glob.glob("interfaces/Default/templates/*.tmpl")),
          ('interfaces/Default/templates/static/stylesheets', glob.glob('interfaces/Default/templates/static/stylesheets/*.*')),
	  ('interfaces/Default/templates/static/stylesheets/colorschemes', glob.glob('interfaces/Default/templates/static/stylesheets/colorschemes/*.*')),
          ('interfaces/Default/templates/static/images', glob.glob('interfaces/Default/templates/static/images/*.ico')),
	  ('interfaces/Default/templates/static/javascript', glob.glob('interfaces/Default/templates/static/javascript/*.js')),

          ('interfaces/smpl/templates', glob.glob("interfaces/smpl/templates/*.*")),
          ('interfaces/smpl/templates/static', glob.glob("interfaces/smpl/templates/static/*.*")),
          ('interfaces/smpl/templates/static/images', glob.glob("interfaces/smpl/templates/static/images/*.*")),
	  ('interfaces/smpl/templates/static/images/nuvola', glob.glob("interfaces/smpl/templates/static/images/nuvola/*.*")),
          ('interfaces/smpl/templates/static/MochiKit', glob.glob("interfaces/smpl/templates/static/MochiKit/*.*")),
          ('interfaces/smpl/templates/static/PlotKit', glob.glob("interfaces/smpl/templates/static/PlotKit/*.*")),
          ('interfaces/smpl/templates/static/excanvas', glob.glob("interfaces/smpl/templates/static/excanvas/*.*")),
          ('interfaces/smpl/templates/static/stylesheets', glob.glob("interfaces/smpl/templates/static/stylesheets/*.*")),
	  ('interfaces/smpl/templates/static/stylesheets/colorschemes', glob.glob("interfaces/smpl/templates/static/stylesheets/colorschemes/*.*")),

          ('interfaces/Plush/templates', glob.glob("interfaces/Plush/templates/*.*")),
          ('interfaces/Plush/templates/static', glob.glob("interfaces/Plush/templates/static/*.*")),
          ('interfaces/Plush/templates/static/images', glob.glob("interfaces/Plush/templates/static/images/*.*")),
          ('interfaces/Plush/templates/static/images/plush-default', glob.glob("interfaces/Plush/templates/static/images/plush-default/*.*")),
          ('interfaces/Plush/templates/static/images/plush-default/config', glob.glob("interfaces/Plush/templates/static/images/plush-default/config/*.*")),
          ('interfaces/Plush/templates/static/images/plush-default/nzo', glob.glob("interfaces/Plush/templates/static/images/plush-default/nzo/*.*")),
          ('interfaces/Plush/templates/static/javascripts', glob.glob("interfaces/Plush/templates/static/javascripts/*.*")),
          ('interfaces/Plush/templates/static/stylesheets', glob.glob("interfaces/Plush/templates/static/stylesheets/*.*")),

	  ('interfaces/iphone/templates', glob.glob("interfaces/iphone/templates/*.*")),
	  ('interfaces/iphone/templates/static', glob.glob("interfaces/iphone/templates/static/*.*")),
	  ('interfaces/iphone/templates/static/iui', glob.glob("interfaces/iphone/templates/static/iui/*.*")),
	  ('interfaces/iphone/templates/MochiKit', glob.glob("interfaces/iphone/templates/static/MochiKit/*.*")),
      ]
)

if py2exe:
    program = [ {'script' : 'SABnzbd.py', 'icon_resources' : [(0, "interfaces/Default/templates/static/images/favicon.ico")] } ]
    options['options'] = {"py2exe": {"bundle_files": 1, "packages": "xml,cherrypy.filters,Cheetah", "optimize": 2, "compressed": 0}}

    # Generate the console-app
    options['console'] = program
    setup(**options)
    try:
        if os.path.exists("dist/%s" % Win32ConsoleName):
            os.remove("dist/%s" % Win32ConsoleName)
        os.rename("dist/%s" % Win32WindowName, "dist/%s" % Win32ConsoleName)
    except:
        print "Cannot create dist/%s" % Win32ConsoleName
        exit(1)
    
    # Make sure that the root files are DOS format
    for file in options['data_files'][0][1]:
        os.system("unix2dos --safe dist/%s" % file)
    os.remove('dist/Sample-PostProc.sh')

    # Generate the windowed-app (skip datafiles now)
    del options['console']
    del options['data_files']
    options['windows'] = program
    setup(**options)

else:
    # Prepare Source distribution package.
    # Make sure all source files are Unix format
    import shutil

    root = 'srcdist'
    root = os.path.normpath(os.path.abspath(root))
    if not os.path.exists(root):
        os.mkdir(root)

    # Copy the data files
    for set in options['data_files']:
        dest, src = set
        ndir = root + '/' + dest
        ndir = os.path.normpath(os.path.abspath(ndir))
        if not os.path.exists(ndir):
            os.makedirs(ndir)
        for file in src:
            shutil.copy2(file, ndir)
            front, ext = os.path.splitext(file)
            base = os.path.basename(file)
            if ext.lower() in ('.py', '.pl', '.txt', '.html', '.css', '.tmpl', ''):
                os.system("dos2unix --quiet --safe %s" % ndir + '/' + base)

    # Copy the script files
    for name in options['scripts']:
        file = os.path.normpath(os.path.abspath(name))
        shutil.copy2(file, root)
        base = os.path.basename(file)
        fullname = os.path.normpath(os.path.abspath(root + '/' + base))
        os.system("dos2unix --quiet --safe %s" % fullname)

    # Copy all content of the packages (but skip backups and pre-compiled stuff)
    for unit in options['packages']:
        unitpath = unit.replace('.','/')
        dest = os.path.normpath(os.path.abspath(root + '/' + unitpath))
        if not os.path.exists(dest):
            os.makedirs(dest)
        for name in glob.glob("%s/*.*" % unitpath):
            file = os.path.normpath(os.path.abspath(name))
            front, ext = os.path.splitext(file)
            base = os.path.basename(file)
            fullname = os.path.normpath(os.path.abspath(dest + '/' + base))
            if ext.lower() not in ('.pyc', '.pyo', '.bak'):
                shutil.copy2(file, dest)
                os.system("dos2unix --quiet --safe %s" % fullname)


setup(**options)
