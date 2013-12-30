
TEMPLATE = subdirs
SUBDIRS += lib_cppunit \
			lib_xerces \
			lib_core

# build must be last:
CONFIG += ordered
SUBDIRS += Fibonacci

lib_core.depends = lib_cppunit
lib_core.depends = lib_xerces
Fibonacci.depends = lib_core

