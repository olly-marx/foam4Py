cmake_minimum_required(VERSION 3.12 FATAL_ERROR)

# Project name
project(foam4Py)

set(CMAKE_PACKAGE_DIR "foam4Py")

# Set CMake variables
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -g")
set(CMAKE_VERBOSE_MAKEFILE ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Include directories
include_directories(${CMAKE_SOURCE_DIR}/foam4Py_cpp/include)

# Add third-party libraries
set(JSON_BuildTests OFF CACHE INTERNAL "")
add_subdirectory(third_party/json)
include_directories(third_party/json/include)
add_subdirectory(third_party/pybind11)
include_directories(third_party/pybind11/include)
add_subdirectory(third_party/pybind11_json)
include_directories(third_party/pybind11_json/include)

# Add FOAM libraries
include(./FOAMConfig.cmake)

# Build the C++ library
find_package(Python ${CMAKE_PYVERSION} REQUIRED COMPONENTS Interpreter Development)
include_directories(${Python_INCLUDE_DIRS})
add_subdirectory(foam4Py_cpp)

# Doxygen documentation
find_package(Doxygen)

if (DOXYGEN_FOUND AND DOXYGEN_BUILD)
    # set input and output files
    set(DOXYGEN_IN ${CMAKE_SOURCE_DIR}/../docs_doxygen/Doxyfile.in)
    set(DOXYGEN_OUT ${CMAKE_SOURCE_DIR}/../docs_doxygen/Doxyfile.out)

    # request to configure the file
    configure_file(${DOXYGEN_IN} ${DOXYGEN_OUT} @ONLY)
    message("Doxygen build started")

    # Note: do not put "ALL" - this builds docs together with application EVERY TIME!
    add_custom_target( docs ALL
        COMMAND ${DOXYGEN_EXECUTABLE} ${DOXYGEN_OUT}
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/../docs_doxygen
        COMMENT "Generating API documentation with Doxygen"
        VERBATIM )
else (DOXYGEN_FOUND)
  message("Doxygen need to be installed to generate the doxygen documentation")
endif (DOXYGEN_FOUND)
