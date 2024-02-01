set(name fvCFDWrapper)

# Add the source files
file(GLOB SOURCES *.C)
file(GLOB HEADERS *.H)

# Add the library
add_library(${name} OBJECT ${SOURCES})
list(APPEND OBJECTS $<TARGET_OBJECTS:${name}>)
set(OBJECTS ${OBJECTS} PARENT_SCOPE)

# Add the installation rules
install(FILES ${HEADERS} 
    DESTINATION ${CMAKE_PACKAGE_DIR}/include/pyBindFOAM/${name})
