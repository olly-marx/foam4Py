set(name pyBlockMesh)

# Add the source files
file(GLOB SOURCES *.C)
file(GLOB HEADERS *.H)

# Add the library
add_library(${name} OBJECT ${SOURCES})
list(APPEND OBJECTS $<TARGET_OBJECTS:${name}>)
set(OBJECTS ${OBJECTS} PARENT_SCOPE)

list(APPEND INCLUDES ${HEADERS})
set(INCLUDES ${INCLUDES} PARENT_SCOPE)

# Add the installation rules
install(FILES ${HEADERS} 
    DESTINATION ${CMAKE_PACKAGE_DIR}/include/${name}
    )
