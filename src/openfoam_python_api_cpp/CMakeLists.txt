set(OBJECTS)

add_subdirectory(meshing)
add_subdirectory(postprocessing)
add_subdirectory(utils)
add_subdirectory(solvers)

# Define the source files for pyBindFOAM library
add_library(openfoam_python STATIC ${OBJECTS})
set_target_properties(openfoam_python PROPERTIES POSITION_INDEPENDENT_CODE ON)

# Link against the foam library
target_link_libraries(openfoam_python ${FOAM_LIBRARIES})
# message("Foam libraries: ${FOAM_LIBRARIES}")

# Link against the python library
target_link_libraries(openfoam_python ${Python_LIBRARIES})
# message("Python libraries: ${Python_LIBRARIES}")

# Link against the json library
target_link_libraries(openfoam_python nlohmann_json::nlohmann_json)

if(CMAKE_PYTHON_BINDINGS)
    # print if python bindings are enabled
    message("Python bindings enabled")
    pybind11_add_module(openfoam_python_api SHARED openfoam_python_api.C)

    # Link against the pyBindFOAM library directly with the full path
    #link_directories(${CMAKE_CURRENT_BINARY_DIR})
    target_link_libraries(openfoam_python_api PRIVATE openfoam_python)
endif()

# Install the pyBindFOAM library
install(TARGETS openfoam_python 
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
    install(TARGETS openfoam_python_api 
	LIBRARY DESTINATION ${CMAKE_PACKAGE_DIR}
	ARCHIVE DESTINATION ${CMAKE_PACKAGE_DIR}
	#RUNTIME DESTINATION ${CMAKE_PACKAGE_DIR}/bin
	#INCLUDES DESTINATION ${CMAKE_PACKAGE_DIR}/include
	)
endif(CMAKE_PYTHON_BINDINGS)
