cmake_minimum_required(VERSION 3.12 FATAL_ERROR)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -g")
set(CMAKE_VERBOSE_MAKEFILE ON)

# Check if MPI is set
if(NOT DEFINED MPI)
	set(MPI False)
endif()

if(MPI)
    set(MPI_ASSUME_NO_BUILTIN_MPI True)
    find_package(MPI REQUIRED COMPONENTS C CXX)
    include_directories(MPI_C_INCLUDE_DIRECTORIES)
    include_directories(MPI_CXX_INCLUDE_DIRECTORIES)
    #add_definitions(-DLARCV_MPI)
endif()

project(pyBindFOAM)

set(CMAKE_PACKAGE_DIR "pyBindFOAMPackage")

include_directories("./")

set(JSON_BuildTests OFF CACHE INTERNAL "")
add_subdirectory(json)                                                           
message("NLOHMANN_JSON_INCLUDE_INSTALL_DIR: ${NLOHMANN_JSON_INCLUDE_INSTALL_DIR}")
include_directories(json/include)

# Check if CMAKE_PYTHON_BINDINGS is set
if(NOT DEFINED CMAKE_PYTHON_BINDINGS)
	set(CMAKE_PYTHON_BINDINGS True)
endif()

if(CMAKE_PYTHON_BINDINGS)

    message("Adding python bindings")
    
    # Many packages need python:
    find_package(Python ${CMAKE_PYVERSION} REQUIRED COMPONENTS  Interpreter Development)
    include_directories(${Python_INCLUDE_DIRS})
    
    message("Adding pybind11")
    add_subdirectory(pybind11)
    include_directories(${PYBIND11_INCLUDE_DIR})
    
    set(pybind11_DIR pybind11)

    # Get pybind11_json
    add_subdirectory(pybind11_json)
    include_directories(pybind11_json/include)

endif(CMAKE_PYTHON_BINDINGS)

# Check in FOAM is set if not set it to TRUE
if(NOT DEFINED FOAM)
	set(FOAM True)
endif()

if(FOAM)
    include(./FOAMConfig.cmake)
endif()

add_subdirectory(pyBindFOAM)
