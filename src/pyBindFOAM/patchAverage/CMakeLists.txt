set(name patchAverage)

# Add the source files
file(GLOB SOURCES *.C)
file(GLOB HEADERS *.H)

# Add the library
add_library(${name} OBJECT ${SOURCES})

# Add the installation rules
install(FILES ${HEADERS} 
    DESTINATION include/pyBindFOAM/patchAverage/${name})
