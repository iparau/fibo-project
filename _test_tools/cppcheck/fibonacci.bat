cppcheck.exe --enable=all -DXERCES_STATIC_LIBRARY -DXERCES_USE_TRANSCODER_WINDOWS -DXERCES_USE_NETACCESSOR_WINSOCK -DXERCES_USE_FILEMGR_WINDOWS -DXERCES_USE_MUTEXMGR_WINDOWS -DXERCES_PATH_DELIMITER_BACKSLASH -DHAVE_STRICMP -DHAVE_STRNICMP -DHAVE_LIMITS_H -DHAVE_SYS_TIMEB_H -DHAVE_FTIME -DHAVE_WCSUPR -DHAVE_WCSLWR -DHAVE_WCSICMP -DHAVE_WCSNICMP ./lib_xerces/srce ./lib_cppunit/srce ./lib_core/srce ./fibonacci/srce -I ./lib_xerces/incl -I ./lib_xerces/incl/xercesc/dom -I ./lib_xerces/incl/xercesc/dom/impl -I ./lib_xerces/incl/xercesc/sax -I ./lib_xerces/incl/xercesc/util -I ./lib_xerces/incl/xercesc/util/MsgLoaders/InMemory -I ./lib_xerces/incl/xercesc/validators/schema/identity -I ./lib_xerces/incl/xercesc/util/MsgLoaders/Win32 -I ./lib_xerces/incl/xercesc/util/Transcoders/Win32 -I ./lib_cppunit/incl -I ./lib_core/incl -I ./fibonacci/incl --template=vs --report-progress --xml-version=2 -v 2> ./_test_tools/cppcheck/fibonacci.xml