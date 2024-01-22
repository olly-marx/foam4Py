cmake_minimum_required(VERSION 3.12 FATAL_ERROR)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -g")
set(CMAKE_COMPILER g++)

enable_language(CXX)

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

#set(CMAKE_INSTALL_PREFIX "..")

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

endif(CMAKE_PYTHON_BINDINGS)

add_subdirectory(pyBindFOAM)
