
TEMPLATE = subdirs
SUBDIRS += lib_cppunit \
			lib_xerces \
			lib_core

# build must be last:
CONFIG += ordered
SUBDIRS += FibonacciTest

lib_core.depends = lib_cppunit
lib_core.depends = lib_xerces
FibonacciTest.depends = lib_core

