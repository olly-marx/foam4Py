# the Basic configuration of foam-extend-5.0 in CMake

# Check valid foam-extend-5.0
if(DEFINED ENV{WM_PROJECT_DIR})
    MESSAGE(STATUS "foam-extend-5.0: " $ENV{WM_PROJECT_DIR})
else()
    message(FATAL_ERROR "The foam-extend-5.0 bashrc is not sourced")
endif(DEFINED ENV{WM_PROJECT_DIR})

set(FOAM_VERSION $ENV{WM_PROJECT_VERSION}) 
set(FOAM_DIR $ENV{WM_PROJECT_DIR})
set(FOAM_LIB_DIR $ENV{FOAM_LIBBIN})
set(FOAM_SRC $ENV{FOAM_SRC})

set(PATH_LIB_OPENMPI "openmpi-system")  # Foundation version
set(DEFINITIONS_COMPILE "-std=c++11 -DWM_ARCH_OPTION=64 -DWM_DP -DWM_LABEL_SIZE=32 -Wall -Wextra -Wno-unused-parameter -Wno-overloaded-virtual -Wno-unused-variable -Wno-unused-local-typedef -Wno-invalid-offsetof -Wno-deprecated-register -Wno-undefined-var-template -O0 -g -DFULLDEBUG -DNoRepository -ftemplate-depth-100 -fPIC")

if(${FOAM_VERSION} MATCHES "v([0-9]*)")       # ESI
    set(PATH_LIB_OPENMPI "sys-openmpi")
    set(DEFINITIONS_COMPILE "-std=c++14 -m64 -pthread -ftrapping-math -DFOAM-EXTEND-5.0=2106 -DWM_DP -DWM_LABEL_SIZE=32 -Wall -Wextra -Wold-style-cast -Wnon-virtual-dtor -Wno-unused-parameter -Wno-invalid-offsetof -Wno-undefined-var-template -Wno-unknown-warning-option  -O3  -DNoRepository -ftemplate-depth-100 -fPIC -DIMPLEMENT_ACTIVATION -Wl,-execute,-undefined,dynamic_lookup")
else()
    # Set definitions for foam-extend-5.0 assuming compilation with gcc and
    # as a shared library
    set(DEFINITIONS_COMPILE "-std=c++11 -m64 -pthread -ftrapping-math -DFOAM-EXTEND-5.0=2106 -DWM_DP -DWM_LABEL_SIZE=32 -Wall -Wextra -Wold-style-cast -Wno-unused-parameter -O3 -DNoRepository -ftemplate-depth-100 -fPIC -DIMPLEMENT_ACTIVATION")
endif()
# =====================================================================================================
# Compiling configure
add_definitions("${DEFINITIONS_COMPILE}")

# ======== OS specific setting =============
if(APPLE)
    add_definitions(" -Ddarwin64 ")
else()
    add_definitions("-Dlinux64")
endif(APPLE)
# ==========================================

# find all of the subdirectories with the FOAM_SRC directory 
file(GLOB FOAM_INCLUDE_DIRS "${FOAM_SRC}/*/lnInclude")

# now include all of the directories
include_directories(${FOAM_INCLUDE_DIRS})
message(STATUS "foam-extend-5.0: include dir='${FOAM_INCLUDE_DIRS}'")
include_directories(${FOAM_SRC}/OSspecific/POSIX)
include_directories(${FOAM_SRC}/OSspecific/POSIX/lnInclude)
include_directories(${FOAM_SRC}/mesh/blockMesh/lnInclude)
include_directories(${FOAM_SRC}/dynamicMesh/dynamicMesh/lnInclude)

# use glob to find all foam libraries
file(GLOB FOAM_LIBRARIES "${FOAM_LIB_DIR}/*.so")

# print a list of the include directories
get_property(dirs DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY INCLUDE_DIRECTORIES)
# foreach(dir ${dirs})
#   message(STATUS "foam-extend-5.0: include dir='${dir}'")
# endforeach()

link_directories(${FOAM_LIB_DIR} ${FOAM_LIB_DIR}/${PATH_LIB_OPENMPI})

