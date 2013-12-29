#Includes common configuration for all subdirectory .pro files.

CONFIG *= warn_on thread debug_and_release

DEFINES *= _REENTRANT LIB

win32 {
	DEFINES *= PLATFORM_WIN32
	CONFIG *= x86 incremental
	QMAKE_LFLAGS *= /LARGEADDRESSAWARE
	#CONFIG *= embed_manifest_exe
	#QMAKE_CXXFLAGS += -EHa
	#QMAKE_CXXFLAGS += /D_CRTDBG_MAP_ALLOC
	QMAKE_LFLAGS += /FIXED:NO
	QMAKE_CXXFLAGS *= /D_CRT_SECURE_NO_WARNINGS
}

unix {
	CONFIG *= largefile
}

unix:!macx {
	DEFINES *= PLATFORM_LINUX
	LIBS *= -lXfixes -lXtst
}

macx {
	DEFINES *= PLATFORM_MAC PLATFORM_NETBSD
	LIBS *= -framework Carbon
}

# The following keeps the generated files at least somewhat separate
# from the source files.
CONFIG(debug,debug|release) {
	DESTDIR     = ./debug
	OBJECTS_DIR = ./debug/objs
} else {
	DESTDIR     = ./release
	OBJECTS_DIR = ./release/objs
}

UI_DIR      = ./.uics
MOC_DIR     = ./.mocs
RCC_DIR     = ./.rccs

DEPENDPATH *= .

# Read from environment variable
CTC_ROOT=$$(CTC_ROOT)

LIB_CORE_DIR		= $$CTC_ROOT/lib/core
LIB_CPPUNIT_DIR		= $$CTC_ROOT/lib/cppunit
LIB_XERCES_DIR		= $$CTC_ROOT/lib/xerces
APP_FIBO_DIR		= $$CTC_ROOT/Fibonacci
APP_FIBOTEST_DIR	= $$BYS_ROOT/FibonacciTest

LIB_CORE_DIR_INC	= $$LIB_CORE_DIR/incl
LIB_CPPUNIT_DIR_INC	= $$LIB_CPPUNIT_DIR/incl
LIB_XERCES_DIR_INC	= $$LIB_XERCES_DIR/incl
APP_FIBO_DIR_INC	= $$APP_FIBO_DIR/incl
APP_FIBOTEST_DIR_INC= $$APP_FIBOTEST_DIR/incl

LIB_CORE_DIR_SRC	= $$LIB_CORE_DIR/srce
LIB_CPPUNIT_DIR_SRC	= $$LIB_CPPUNIT_DIR/srce
LIB_XERCES_DIR_SRC	= $$LIB_XERCES_DIR/srce
APP_FIBO_DIR_SRC	= $$APP_FIBO_DIR/srce
APP_FIBOTEST_DIR_SRC= $$APP_FIBOTEST_DIR/srce

LIB_CORE_DIR_RLS	= $$LIB_CORE_DIR/release
LIB_CPPUNIT_DIR_RLS	= $$LIB_CPPUNIT_DIR/release
LIB_XERCES_DIR_RLS	= $$LIB_XERCES_DIR/release
APP_FIBO_DIR_RLS	= $$APP_FIBO_DIR/release
APP_FIBOTEST_DIR_RLS= $$APP_FIBOTEST_DIR/release

LIB_CORE_DIR_DBG	= $$LIB_CORE_DIR/debug
LIB_CPPUNIT_DIR_DBG	= $$LIB_CPPUNIT_DIR/debug
LIB_XERCES_DIR_DBG	= $$LIB_XERCES_DIR/debug
APP_FIBO_DIR_DBG	= $$APP_FIBO_DIR/debug
APP_FIBOTEST_DIR_DBG= $$APP_FIBOTEST_DIR/debug
