#!/usr/bin/python

import sys, os, shutil

#the list contains the targets accepted for build
targets_list = ['clean', 'libs', 'fibonacci', 'fibonaccitest', 'all']

#the list contains the dependencies of the modules
#<module_to_build> contains the list of dependent modules
dependancies = {
	'lib_cppunit' : [],
	'lib_xerces' : [],
	'lib_core' :  ['lib_cppunit','lib_xerces'],
	'libs' : ['lib_core'],
	'fibonacci' : ['lib_core'],
	'fibonaccitest' : ['lib_core'],
	'all': ['fibonacci', 'fibonaccitest']
	}

#the list contains the build information for the module
#<module_to_build> contains the path, the project file, enable build, use Qt make or vcproj make, enable build translations	(qt only), copy brand resources (for vcproj make)
modules_list = {
	'lib_cppunit' : [('lib_cppunit', 'lib_cppunit.pro', True, True, False, False)],
	'lib_xerces' :  [('lib_xerces', 'lib_xerces.pro', True, True, False, False)],
	'lib_core' : [('lib_core', 'lib_core.pro', True, True, False, False)],
	'libs' : [('', 'ctc_libs.pro', False, True, False, False)],
	'fibonacci' : [('fibonacci', 'fibonacci.pro', True, True, False, False),
			('', 'ctc_fibonacci.pro', False, True, False, False)],
	'fibonaccitest' : [('fibonaccitest', 'fibonaccitest.pro', True, True, False, False),
				('', 'ctc_fibonaccitest.pro', False, True, False, False)]
	}

builded = {
	'lib_cppunit' : False,
	'lib_xerces' :  False,
	'lib_core' : False,
	'libs' : False,
	'fibonacci' : False,
    'fibonaccitest' : False,
    'all' : False
	}

#build flag, win32 name, mac name, linux name, enable upx, enable sign
modules_output_files = {
	'lib_cppunit' : [(False, '', '', '', False, False)],
	'lib_xerces' :  [(False, '', '', '', False, False)],
	'lib_core' : [(False, '', '', '', False, False)],
	'libs' : [(False, '', '', '', False, False)],
	'fibonacci' : [(True, 'fibonacci.exe', 'fibonacci', 'fibonacci', False, False)],
	'fibonaccitest' : [(True, 'fibonaccitest.exe', 'fibonaccitest', 'fibonaccitest', False, False)]
	}

# key file, key pass, win32 path, mac path, linux path
signs_keys_list = {
	'' : [('', '', '', '', '')],
	}

#path name, file name
signs_tools_list = {
	'nt' : [('_build_tools/win32/tools', 'signtool.exe')],
	'mac' : [('', 'codesign')],
	'linux' : []
	}

#path name, file name
upx_tools_list = {
	'nt' : [('_build_tools/win32/tools', 'upx.exe')],
	'mac' : [('_build_tools/mac/tools', 'upx')],
	'linux' : [('_build_tools/linux/tools', 'upx')]
	}

def active_params():
	print ""
	print "Active parameters are:"
	print ""

	print " - product: " + producttobuild

	if DEBUG_RELEASE == False:
		if BUILD_MODE == False:
			print " - type: release"
		else:
			print " - type: debug"
	else:
		print " - type: debug and release"

	print "..."

	global current_os
	if current_os == "nt":
		if MANIFEST == True:
			print " - generate manifest: enabled"
		else:
			print " - generate manifest: disabled"

		if VCPROJ == True:
			print " - generate vcproj: enabled"
		else:
			print " - generate vcproj: disabled"

	if current_os == "mac":
		if MACDEVEL_LIC == True:
			print " - license type: Mac Developer"
		else:
			print " - license type: Developer ID Application"

def syntax():
	print "Syntax:"

	print "First parameter should contain the customer name: 'clean', 'libs', 'fibonacci', 'fibonaccitest' or 'all'"
	print "Optional parameters:"
	print "MA - Generate Manifest"
	print "DB - Debug Mode Build (by default: Release Mode)"
	print "DR - Debug and Release Mode Build"
	print "NK - No kit"
	print "VC - Generate vcproj files"
	print "DL - Use Mac Developer license, default is Developer ID license (Mac Only!)"

	print ""

def exit_usage():
	syntax()
	sys.exit(1)

def do_exec(cmdline, check):
	print cmdline
	ret = os.system(cmdline)

	if (check == True):
		if ret != 0:
			print "Error detected! Build aborted!"
			sys.exit(1)

def copytree(src, dst, symlinks=False, ignore=None):
	names = os.listdir(src)
	if ignore is not None:
		ignored_names = ignore(src, names)
	else:
		ignored_names = set()

	ret = os.access(dst, os.F_OK)

	if (False == ret):
		os.makedirs(dst)

	errors = []
	for name in names:
		if name in ignored_names:
			continue
		srcname = os.path.join(src, name)
		dstname = os.path.join(dst, name)
		try:
			if symlinks and os.path.islink(srcname):
				linkto = os.readlink(srcname)
				os.symlink(linkto, dstname)
			elif os.path.isdir(srcname):
				copytree(srcname, dstname, symlinks, ignore)
			else:
				shutil.copy2(srcname, dstname)
			# XXX What about devices, sockets etc.?
		except (IOError, os.error) as why:
			errors.append((srcname, dstname, str(why)))

	try:
		shutil.copystat(src, dst)
	except WindowsError:
		# can't copy file access times on Windows
		pass
	except OSError as why:
		errors.extend((src, dst, str(why)))
	if errors:
		raise Error(errors)

def do_copy(srcname, dstname):
	print "do_copy src: " + srcname + " dst: " + dstname

	if os.path.isdir(srcname):
		copytree(srcname, dstname)
	else:
		shutil.copy2(srcname, dstname)


def do_module_clean(moduletoclean):
	print "Cleaning module: " + moduletoclean
	#Dependancies handling
	for dep in dependancies[moduletoclean]:
		do_module_clean(dep)

	if not moduletoclean in modules_list.keys():
		return

	for moduleitem in modules_list[moduletoclean]:
		subdir = CTC_ROOT + os.sep + moduleitem[0]
		if (True == os.path.lexists(subdir + os.sep + MAKEFILENAME)):

			cmdline = 'cd ' + subdir
			cmdline += ' && ' + MAKE + MAKEFILENAME + ' clean'

			do_exec(cmdline, False)

			os.remove( subdir + os.sep + MAKEFILENAME )

def do_module_build(moduletobuild):
	#check first if we had not already builded this module
	if not builded[moduletobuild]:
		print 'Building module: ' + moduletobuild
		#Dependancies handling
		for dep in dependancies[moduletobuild]:
			do_module_build(dep)

		if moduletobuild in modules_list.keys():
			buildMakeFile = MAKEFILENAME
			vcBuildCmd = 'MSBuild.exe '
			vcBuildParam = '/m:4 /Verbosity:normal /DetailedSummary'

			for moduleitem in modules_list[moduletobuild]:
				subdir = CTC_ROOT + os.sep + moduleitem[0]

				profile   = moduleitem[1] # .pro file name
				make_flag = moduleitem[2]
				qt_flag   = moduleitem[3]
				tr_flag   = moduleitem[4]
				res_flag  = moduleitem[5]
				
				#should we copy the brand dependent resources?
				#if (True == res_flag):
					#do_copy(subdir + os.sep + 'res_' + current_brand, subdir + os.sep + 'res');

				#should we build using qmake?
				if (True == qt_flag):

					if tr_flag:
						print "Releasing the translation files"
						cmdline = 'cd ' + subdir
						cmdline += ' && lrelease -silent ' + profile

						do_exec(cmdline, True)

					if VCPROJ:
						print "Generating the vcxproj files"
						cmdline = 'cd ' + subdir
						cmdline += ' && ' + QMAKE + ' -tp vc ' + profile

						do_exec(cmdline, True)

					#create the MAKEFILE
					cmdline = 'cd ' + subdir
					cmdline += ' && ' + QMAKE + ' -o ' + buildMakeFile + ' ' + profile

					do_exec(cmdline, True)

					if (True == make_flag):
						if DEBUG_RELEASE == False:
							if BUILD_MODE == True:
								print "Executing debug mode build"
								cmdline = 'cd ' + subdir
								cmdline += ' && ' + MAKE + buildMakeFile + ' debug'

								if current_os != "nt":
									cmdline += ' -j4'

								do_exec(cmdline, True)
							else:
								print "Executing release mode build"
								cmdline = 'cd ' + subdir
								cmdline += ' && ' + MAKE + buildMakeFile + ' release'

								if current_os != "nt":
									cmdline += ' -j4'

								do_exec(cmdline, True)

							#do the executable distrib
							do_module_distrib(moduletobuild, subdir)

						else:
							print "Executing debug and release mode build"
							cmdline = 'cd ' + subdir
							cmdline += ' && ' + MAKE + buildMakeFile + ' debug'

							if current_os != "nt":
								cmdline += ' -j4'

							do_exec(cmdline, True)

							cmdline = 'cd ' + subdir
							cmdline += ' && ' + MAKE + buildMakeFile + ' release'

							if current_os != "nt":
								cmdline += ' -j4'

							do_exec(cmdline, True)

							#do the executable distrib
							do_module_distrib(moduletobuild, subdir)

				#we build using vcproj
				else:
					if (True == make_flag):
						if DEBUG_RELEASE == False:
							if BUILD_MODE == True:
								print "Executing debug mode build"
								cmdline = 'cd ' + subdir
								cmdline += ' && ' + vcBuildCmd + vcBuildParam + ' /p:Configuration="Debug"' + ' ' + profile

								do_exec(cmdline, True)

							else:
								print "Executing release mode build"
								cmdline = 'cd ' + subdir
								cmdline += ' && ' + vcBuildCmd + vcBuildParam + ' /p:Configuration="Release"' + ' ' + profile

								do_exec(cmdline, True)

						else:
							print "Executing debug and release mode build"
							cmdline = 'cd ' + subdir
							cmdline += ' && ' + vcBuildCmd + vcBuildParam + ' /p:Configuration="Debug"' + ' ' + profile

							do_exec(cmdline, True)
							cmdline = 'cd ' + subdir
							cmdline += ' && ' + vcBuildCmd + vcBuildParam + ' /p:Configuration="Release"' + ' ' + profile

							do_exec(cmdline, True)

						#do the executable distrib
						do_module_distrib(moduletobuild, subdir)

		builded[moduletobuild] = True

	else:
		cmdline = 'rem ' + moduletobuild + ' has already been build'
		print cmdline

def do_module_distrib(moduletodistrib, subdir):
	if moduletodistrib in modules_output_files.keys():
		print 'module distrib: ' + moduletodistrib
		for builditem in modules_output_files[moduletodistrib]:
			exe_flag = builditem[0] #do we expect an executable output?

			if (True == exe_flag):
				print "Distributing module: " + moduletodistrib
				print "Current subdir: " + subdir

				distribPath = CTC_ROOT + os.sep + "_distrib"
				ret = os.access(distribPath, os.F_OK)

				if (False == ret):
					os.mkdir(distribPath)

				modulePath = distribPath + os.sep + moduletodistrib
				ret = os.access(modulePath, os.F_OK)

				if (False == ret):
					os.mkdir(modulePath)

				exe_win32 = ''
				exe_mac = ''
				exe_linux = ''

				exe_win32 = builditem[1] # win32 executable file name
				exe_mac = builditem[2] # mac executable file name
				exe_linux = builditem[3] # linux executable file name

				exe_name = exe_win32

				global current_os
				if current_os == "mac":
					exe_name = exe_mac + '.app'
				elif current_os == "linux":
					exe_name = exe_linux

				print "Distributing executable: " + exe_name

				upx_flag = builditem[4] # should we upx?
				sign_flag = builditem[5] # should we sign?

				#copy executable to its module path
				if DEBUG_RELEASE == False:
					if BUILD_MODE == True:
						print 'Executing debug mode distrib'

						srcPath = subdir + os.sep + 'debug'
						#deploy the qt dependencies on mac
						if current_os == "mac":
							print 'Call macdeployqt: ' + srcPath
							cmdline = 'cd ' + srcPath
							cmdline += ' && macdeployqt ' + exe_name

							do_exec(cmdline, True)

						do_copy( srcPath + os.sep + exe_name, modulePath + os.sep + exe_name);
					else:
						print 'Executing release mode distrib'

						srcPath = subdir + os.sep + 'release'
						#deploy the qt dependencies on mac
						if current_os == "mac":
							print 'Call macdeployqt: ' + srcPath
							cmdline = 'cd ' + srcPath
							cmdline += ' && macdeployqt ' + exe_name

							do_exec(cmdline, True)

						do_copy( srcPath + os.sep + exe_name, modulePath + os.sep + exe_name);
				else:
					print 'Executing debug and release mode distrib'

					srcPath = subdir + os.sep + 'debug'
					#deploy the qt dependencies on mac
					if current_os == "mac":
						print 'Call macdeployqt: ' + srcPath
						cmdline = 'cd ' + srcPath
						cmdline += ' && macdeployqt ' + exe_name

						do_exec(cmdline, True)

					do_copy( srcPath + os.sep + exe_name, modulePath + os.sep + exe_name);

					srcPath = subdir + os.sep + 'release'
					#deploy the qt dependencies on mac
					if current_os == "mac":
						print 'Call macdeployqt: ' + srcPath
						cmdline = 'cd ' + srcPath
						cmdline += ' && macdeployqt ' + exe_name

						do_exec(cmdline, True)

					do_copy( srcPath + os.sep + exe_name, modulePath + os.sep + exe_name);

				#deploy the qt dependencies on mac
				#if current_os == "mac":
				#print 'Call macdeployqt dmg: ' + srcPath
					#cmdline = 'cd ' + modulePath
					#cmdline += ' && macdeployqt ' + exe_name + ' -dmg'

					#do_exec(cmdline, True)


				if (True == sign_flag):
					for signitem in signs_tools_list[current_os]:
						tool_dir = CTC_ROOT + os.sep + signitem[0]
						sign_tool = signitem[1] # sign tool file name

						for keyitem in signs_keys_list[current_brand]:
							key_file = keyitem[0] # key file name
							key_pass = keyitem[1] # key password
							key_dir = CTC_ROOT + os.sep + keyitem[2]

							if (current_os == "mac"):
								
								signature = '\"Developer ID Application:\"'
								if MACDEVEL_LIC == True:
									signature = '\"Mac Developer:\"'
									
								#since 10.9 we have to sign all the sub-modules and all the plugins from app bundle
								#sign QtCore sub-module
								cmdline = 'cd ' + modulePath
								cmdline += ' && cp $QTDIR/lib/QtCore.framework/Contents/Info.plist ' + modulePath + os.sep + exe_name + '/Contents/Frameworks/QtCore.framework/Resources/'
								cmdline += ' && ' + sign_tool + ' --force --verify --verbose --sign ' + signature + ' ' + modulePath + os.sep + exe_name + '/Contents/Frameworks/QtCore.framework'
								
								do_exec(cmdline, False)
								
								#sign QtGui sub-module
								cmdline = 'cd ' + modulePath
								cmdline += ' && cp $QTDIR/lib/QtGui.framework/Contents/Info.plist ' + modulePath + os.sep + exe_name + '/Contents/Frameworks/QtGui.framework/Resources/'
								cmdline += ' && ' + sign_tool + ' --force --verify --verbose --sign ' + signature + ' ' + modulePath + os.sep + exe_name + '/Contents/Frameworks/QtGui.framework'
								
								do_exec(cmdline, False)
								
								#sign QtNetwork sub-module
								cmdline = 'cd ' + modulePath
								cmdline += ' && cp $QTDIR/lib/QtNetwork.framework/Contents/Info.plist ' + modulePath + os.sep + exe_name + '/Contents/Frameworks/QtNetwork.framework/Resources/'
								cmdline += ' && ' + sign_tool + ' --force --verify --verbose --sign ' + signature + ' ' + modulePath + os.sep + exe_name + '/Contents/Frameworks/QtNetwork.framework'
								
								do_exec(cmdline, False)
								
								#sign QtOpenGL sub-module
								cmdline = 'cd ' + modulePath
								cmdline += ' && cp $QTDIR/lib/QtOpenGL.framework/Contents/Info.plist ' + modulePath + os.sep + exe_name + '/Contents/Frameworks/QtOpenGL.framework/Resources/'
								cmdline += ' && ' + sign_tool + ' --force --verify --verbose --sign ' + signature + ' ' + modulePath + os.sep + exe_name + '/Contents/Frameworks/QtOpenGL.framework'
								
								do_exec(cmdline, False)
								
								#sign QtXml sub-module
								cmdline = 'cd ' + modulePath
								cmdline += ' && cp $QTDIR/lib/QtXml.framework/Contents/Info.plist ' + modulePath + os.sep + exe_name + '/Contents/Frameworks/QtXml.framework/Resources/'
								cmdline += ' && ' + sign_tool + ' --force --verify --verbose --sign ' + signature + ' ' + modulePath + os.sep + exe_name + '/Contents/Frameworks/QtXml.framework'
								
								do_exec(cmdline, False)
								
								#sign accesible plugin
								cmdline = 'cd ' + modulePath
								cmdline += ' && ' + sign_tool + ' --force --verify --verbose --sign ' + signature + ' ' + modulePath + os.sep + exe_name + '/Contents/PlugIns/accessible/libqtaccessiblewidgets.dylib'
								
								do_exec(cmdline, False)
								
								#sign bearer plugin
								cmdline = 'cd ' + modulePath
								cmdline += ' && ' + sign_tool + ' --force --verify --verbose --sign ' + signature + ' ' + modulePath + os.sep + exe_name + '/Contents/PlugIns/bearer/libqgenericbearer.dylib'
								
								do_exec(cmdline, False)
								
								#sign imageformats ico plugin
								cmdline = 'cd ' + modulePath
								cmdline += ' && ' + sign_tool + ' --force --verify --verbose --sign ' + signature + ' ' + modulePath + os.sep + exe_name + '/Contents/PlugIns/imageformats/libqico.dylib'
								
								do_exec(cmdline, False)
								
								#sign imageformats jpeg plugin
								cmdline = 'cd ' + modulePath
								cmdline += ' && ' + sign_tool + ' --force --verify --verbose --sign ' + signature + ' ' + modulePath + os.sep + exe_name + '/Contents/PlugIns/imageformats/libqjpeg.dylib'
								
								do_exec(cmdline, False)
								
								#sign imageformats mng plugin
								cmdline = 'cd ' + modulePath
								cmdline += ' && ' + sign_tool + ' --force --verify --verbose --sign ' + signature + ' ' + modulePath + os.sep + exe_name + '/Contents/PlugIns/imageformats/libqmng.dylib'
								
								do_exec(cmdline, False)
								
								#sign imageformats tga plugin
								cmdline = 'cd ' + modulePath
								cmdline += ' && ' + sign_tool + ' --force --verify --verbose --sign ' + signature + ' ' + modulePath + os.sep + exe_name + '/Contents/PlugIns/imageformats/libqtga.dylib'
								
								do_exec(cmdline, False)
								
								#sign imageformats tiff plugin
								cmdline = 'cd ' + modulePath
								cmdline += ' && ' + sign_tool + ' --force --verify --verbose --sign ' + signature + ' ' + modulePath + os.sep + exe_name + '/Contents/PlugIns/imageformats/libqtiff.dylib'
								
								do_exec(cmdline, False)
								
								#now we can sign the module application bundle
								cmdline = 'cd ' + modulePath
								cmdline += ' && ' + sign_tool + ' --force --verify --verbose --sign ' + signature + ' ' + modulePath + os.sep + exe_name
										
								do_exec(cmdline, False)
							else:
								if (current_os == "linux"): #currently not implemented for linux
									print "Sign not implemented for linux"
								else:
									print "Executing sign"
									cmdline = 'cd ' + modulePath
									cmdline += ' && ' + tool_dir + os.sep + sign_tool + ' sign /f ' + key_dir + os.sep + key_file + ' /p ' + key_pass + ' /d ' +  exe_name + ' /t http://timestamp.verisign.com/scripts/timstamp.dll ' + modulePath + os.sep + exe_name

									do_exec(cmdline, False)

				if (True == upx_flag):
					for compressitem in upx_tools_list[current_os]:
						tool_dir = CTC_ROOT + os.sep + compressitem[0]
						compress_tool = compressitem[1] # compress tool file name

						if (current_os == "mac"): #mac is a special case
							print "Executing upx disabled on Mac"
						else:
							print "Executing upx"
							cmdline = 'cd ' + modulePath

							if (current_os == "mac"): #mac is a special case
								cmdline += ' && ' + tool_dir + os.sep + compress_tool + ' --lzma --best --compress-icons=0 ' + exe_name + os.sep + 'Contents' + os.sep + 'MacOS' + os.sep + exe_mac
							else:
								cmdline += ' && ' + tool_dir + os.sep + compress_tool + ' --lzma --best --compress-icons=0 ' + exe_name

							do_exec(cmdline, True)
							
				
				#build the dmg file on mac
				if current_os == "mac":
					print 'Build dmg file on: ' + srcPath
					cmdline = 'cd ' + modulePath
					cmdline += ' && hdiutil create -srcfolder ' + exe_name + ' -format UDBZ -quiet ' + exe_mac + '.dmg'

					do_exec(cmdline, True)

					cmdline = 'cd ' + modulePath
					cmdline += ' && hdiutil internet-enable -yes ' + exe_mac + '.dmg'
					
					do_exec(cmdline, True)
					
				#build the ditto file on mac
				if current_os == "mac":
					print 'Build zip with ditto file on: ' + srcPath
					cmdline = 'cd ' + modulePath
					cmdline += ' && ditto -ck --rsrc --sequesterRsrc --keepParent ' + exe_name + ' ' + exe_name + '.zip'

					do_exec(cmdline, True)
					
				print 'Distributing executable: ' + exe_name + ' completed'
					
def do_module(moduletomake):
	print 'make module ' + moduletomake

	if (moduletomake =="clean"):
		do_module_clean("all")
		return

	#we build the module
	do_module_build(moduletomake)
	return


producttobuild = ''

CTC_ROOT = ''
current_os = 'nt'

mode_debug = 'debug'
mode_release = 'release'
mode_debug_release = 'debug_and_release'

BUILD_MODE=False
DEBUG_RELEASE=False
REBUILD=False
MANIFEST=False
VCPROJ=False
MACDEVEL_LIC=False

#program startup
if len(sys.argv) < 2:
	exit_usage()

if not sys.argv[1] in targets_list:
	print 'Product ' + sys.argv[1] + ' not found'
	exit_usage()

print ''

producttobuild = sys.argv[1]
print 'Product to build: ' + producttobuild

for argc in sys.argv:
	if argc=="DB":
		BUILD_MODE = True
		continue
	if argc=="db":
		BUILD_MODE = True
		continue
	if argc=="FB":
		REBUILD = True
		continue
	if argc=="fb":
		REBUILD = True
		continue
	if argc=="MA":
		MANIFEST = True
		continue
	if argc=="ma":
		MANIFEST = True
		continue
	if argc=="DR":
		DEBUG_RELEASE = True
		continue
	if argc=="dr":
		DEBUG_RELEASE = True
		continue
	if argc=="VC":
		VCPROJ = True
		continue
	if argc=="vc":
		VCPROJ = True
		continue
	if argc=="DL":
		MACDEVEL_LIC = True
		continue
	if argc=="dl":
		MACDEVEL_LIC = True
		continue

print ''

ENVPATH_SEPARATOR = os.pathsep
QTDIR = os.getenv("QTDIR")
QMAKE = QTDIR + os.sep + "bin" + os.sep + "qmake"

if os.name == "posix":
	if sys.platform == "darwin":
		print 'Identified OSTYPE: Mac OSX'
		MAKEFILENAME='MacMakefile'
		current_os = 'mac'
	else:
		print 'Identified OSTYPE: Linux'
		MAKEFILENAME='LinMakefile'
		current_os = 'linux'
	MAKE='make -f '

else:
	if os.name == "nt":
		print 'Identified OSTYPE: Windows NT'
		MAKEFILENAME='WinMakefile'
		MAKE='nmake /f '
		current_os = 'nt'
	else:
		print "Unknown OSTYPE: Build Cancelled!"
		sys.exit(1)

active_params()

print ''

#This environment variable is used by common.inc
CTC_ROOT = os.getcwd()
os.environ['CTC_ROOT'] = os.getcwd()

print 'Build ROOT: ' + CTC_ROOT
print 'Build qmake: ' + QMAKE
print ''

print 'Cleaning up _distrib folder ...'

distribPath = CTC_ROOT + os.sep + '_distrib'
ret = os.access(distribPath, os.F_OK)

if (True == ret):
	shutil.rmtree(distribPath, True)

do_module(producttobuild)

