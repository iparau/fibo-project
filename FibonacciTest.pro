
TEMPLATE = subdirs
SUBDIRS += ./lib/core \
        ./lib/cppunit \
	./lib/xerces \

# build must be last:
CONFIG += ordered
SUBDIRS += ./FibonacciTest

core.depends = cppunit
core.depends = xerces
FibonacciTest.depends = core

