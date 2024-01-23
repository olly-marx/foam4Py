set(name patchAverage)

# Add the source files
file(GLOB SOURCE ${name}.C)
file(GLOB HEADER ${name}.H)

# Add the library
add_library(${name} OBJECT ${SOURCE})
list(APPEND OBJECTS $<TARGET_OBJECTS:${name}>)
set(OBJECTS ${OBJECTS} PARENT_SCOPE)

# Add the installation rules
install(FILES ${HEADER} 
    DESTINATION ${CMAKE_PACKAGE_DIR}/include/pyBindFOAM/${name})
