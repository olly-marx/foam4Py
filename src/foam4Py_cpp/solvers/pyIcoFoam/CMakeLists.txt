set(name pyIcoFoam)

# Add the source files
file(GLOB SOURCES ${name}.C)
file(GLOB HEADERS ${name}.H)

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
