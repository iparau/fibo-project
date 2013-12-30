
TEMPLATE = subdirs
SUBDIRS += lib/core \
			lib/cppunit \
			lib/xerces

# build must be last:
CONFIG += ordered
SUBDIRS += Fibonacci

core.depends = cppunit
core.depends = xerces
Fibonacci.depends = core

