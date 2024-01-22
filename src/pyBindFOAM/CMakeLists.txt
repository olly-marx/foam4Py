add_library(pyBindFOAM SHARED
    $<TARGET_OBJECTS:patchAverage>
    )

# Check in FOAM is set if not set it to TRUE
if(NOT DEFINED FOAM)
	set(FOAM True)
endif()

if(FOAM)
    include(../FOAMConfig.cmake)
endif()

# Link finiteVolume library
#target_link_libraries(pyBindFOAM finiteVolume)

# Link against the python library
target_link_libraries(pyBindFOAM ${Python_LIBRARIES})

add_subdirectory(patchAverage)

if(CMAKE_PYTHON_BINDINGS)
    pybind11_add_module(pyBindFOAMMods SHARED pyBindFOAMMods.C)

    set_target_properties(pyBindFOAMMods PROPERTIES SKIP_BUILD_RPATH FALSE)

    set_target_properties(pyBindFOAMMods PROPERTIES BUILD_WITH_INSTALL_RPATH TRUE)

    target_link_libraries(pyBindFOAMMods PRIVATE pyBindFOAM)

    set_target_properties(pyBindFOAMMods PROPERTIES INSTALL_RPATH "$ORIGIN/lib")

    set_target_properties(pyBindFOAMMods PROPERTIES INSTALL_RPATH_USE_LINK_PATH TRUE)
endif()

# Install the foamBindMods library
install(TARGETS pyBindFOAM 
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
    INCLUDES DESTINATION include
    )

# Define the location of the header files, for doc generation
set(FOAM_BIND_MODS_INCLUDE_DIR include)
message("FOAM_BIND_MODS_INCLUDE_DIR: ${FOAM_BIND_MODS_INCLUDE_DIR}")

if(CMAKE_PYTHON_BINDINGS)
    # Install the pyBindFOAMMods library
    install(TARGETS pyBindFOAMMods 
	LIBRARY DESTINATION lib
	ARCHIVE DESTINATION lib
	#RUNTIME DESTINATION ${CMAKE_PACKAGE_DIR}/bin
	#INCLUDES DESTINATION ${CMAKE_PACKAGE_DIR}/include
	)

endif(CMAKE_PYTHON_BINDINGS)
