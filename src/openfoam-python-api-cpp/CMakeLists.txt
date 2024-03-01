set(OBJECTS)

add_subdirectory(patchAverage)
add_subdirectory(fvCFDWrapper)
add_subdirectory(utils)
add_subdirectory(pyBlockMesh)

# Define the source files for pyBindFOAM library
add_library(pyBindFOAM STATIC ${OBJECTS})
set_target_properties(pyBindFOAM PROPERTIES POSITION_INDEPENDENT_CODE ON)

# Link against the foam library
target_link_libraries(pyBindFOAM ${FOAM_LIBRARIES})
# message("Foam libraries: ${FOAM_LIBRARIES}")

# Link against the python library
target_link_libraries(pyBindFOAM ${Python_LIBRARIES})
# message("Python libraries: ${Python_LIBRARIES}")

# Link against the json library
target_link_libraries(pyBindFOAM nlohmann_json::nlohmann_json)

if(CMAKE_PYTHON_BINDINGS)
    # print if python bindings are enabled
    message("Python bindings enabled")
    pybind11_add_module(pyBindFOAMMods SHARED pyBindFOAMMods.C)

    # Link against the pyBindFOAM library directly with the full path
    #link_directories(${CMAKE_CURRENT_BINARY_DIR})
    target_link_libraries(pyBindFOAMMods PRIVATE pyBindFOAM)
endif()

# Install the pyBindFOAM library
install(TARGETS pyBindFOAM 
    LIBRARY DESTINATION ${CMAKE_PACKAGE_DIR}/lib
    ARCHIVE DESTINATION ${CMAKE_PACKAGE_DIR}/lib
    RUNTIME DESTINATION ${CMAKE_PACKAGE_DIR}/bin
    INCLUDES DESTINATION ${CMAKE_PACKAGE_DIR}/include
    )

# Define the location of the header files, for doc generation
set(PYBINDFOAM_PUBLIC_HEADER_DIR ${CMAKE_PACKAGE_DIR}/include)
message("Header dir: ${PYBINDFOAM_PUBLIC_HEADER_DIR}")

if(CMAKE_PYTHON_BINDINGS)
    # Install the pyBindFOAMMods library
    install(TARGETS pyBindFOAMMods 
	LIBRARY DESTINATION ${CMAKE_PACKAGE_DIR}
	ARCHIVE DESTINATION ${CMAKE_PACKAGE_DIR}
	#RUNTIME DESTINATION ${CMAKE_PACKAGE_DIR}/bin
	#INCLUDES DESTINATION ${CMAKE_PACKAGE_DIR}/include
	)
endif(CMAKE_PYTHON_BINDINGS)
