
TEMPLATE = subdirs
SUBDIRS += lib_cppunit \
			lib_xerces \
			lib_core

# build must be last:
CONFIG += ordered
SUBDIRS += fibonacci

lib_core.depends = lib_cppunit
lib_core.depends = lib_xerces
fibonacci.depends = lib_core

