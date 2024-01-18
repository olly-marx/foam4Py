add_subdirectory(patchAverage)

add_library(foamBindMods SHARED
    $<TARGET_OBJECTS:patchAverage>
    )

# Link against the python library
target_link_libraries(foamBindMods ${Python_LIBRARIES})

if(FOAM)
    set(FOAM_ROOT_DIR /home/ojm40/foam/foam-extend-5.0)

    # Set the FOAM_LIBBIN variable to the location of the OpenFOAM libraries
    set(FOAM_LIBBIN ${FOAM_ROOT_DIR}/lib/linux64GccDPInt32Opt)

    add_library(foam STATIC IMPORTED)
    set_target_properties(foam PROPERTIES IMPORTED_LOCATION ${FOAM_LIBBIN}/libfiniteVolume.so)

    # print out the location of the imported library
    message("Linking to OpenFOAM libraries: ${FOAM_LIBBIN}")

    # Now link the imported library to your executable
    target_link_libraries(foamBindMods foam)
endif()

if(CMAKE_PYTHON_BINDINGS)
    pybind11_add_module(pyBindFOAM SHARED pyBindFOAM.C)

    set_target_properties(pyBindFOAM PROPERTIES SKIP_BUILD_RPATH FALSE)

    set_target_properties(pyBindFOAM PROPERTIES BUILD_WITH_INSTALL_RPATH TRUE)

    target_link_libraries(pyBindFOAM PRIVATE foamBindMods)

    set_target_properties(pyBindFOAM PROPERTIES INSTALL_RPATH "$ORIGIN/lib")

    set_target_properties(pyBindFOAM PROPERTIES INSTALL_RPATH_USE_LINK_PATH TRUE)
endif()

# Install the foamBindMods library
install(TARGETS foamBindMods 
    LIBRARY DESTINATION ${CMAKE_PACKAGE_DIR}/lib
    ARCHIVE DESTINATION ${CMAKE_PACKAGE_DIR}/lib
    RUNTIME DESTINATION ${CMAKE_PACKAGE_DIR}/bin
    INCLUDES DESTINATION ${CMAKE_PACKAGE_DIR}/include
    )

# Define the location of the header files, for doc generation
set(FOAM_BIND_MODS_INCLUDE_DIR ${CMAKE_PACKAGE_DIR}/include)
message("FOAM_BIND_MODS_INCLUDE_DIR: ${FOAM_BIND_MODS_INCLUDE_DIR}")

if(CMAKE_PYTHON_BINDINGS)
    # Install the pyBindFOAM library
    install(TARGETS pyBindFOAM 
	LIBRARY DESTINATION ${CMAKE_PACKAGE_DIR}
	ARCHIVE DESTINATION ${CMAKE_PACKAGE_DIR}
	#RUNTIME DESTINATION ${CMAKE_PACKAGE_DIR}/bin
	#INCLUDES DESTINATION ${CMAKE_PACKAGE_DIR}/include
	)

endif(CMAKE_PYTHON_BINDINGS)
