# Set objects and includes
set(OBJECTS)
set(INCLUDES)

# Add subdirectories for C++ components
add_subdirectory(meshing)
add_subdirectory(postprocessing)
add_subdirectory(utils)
#add_subdirectory(solvers)

# Create symlinks for header files
foreach(HEADER ${INCLUDES})
    get_filename_component(HEADER_NAME ${HEADER} NAME)
    set(include_dir "${CMAKE_SOURCE_DIR}/foam4Py_cpp/include")
    file(CREATE_LINK "${HEADER}" "${include_dir}/${HEADER_NAME}" SYMBOLIC)
endforeach()

# Include directories
include_directories(${CMAKE_SOURCE_DIR}/foam4Py_cpp/include)

# Define the source files for the library
add_library(foam4Py_cpp STATIC ${OBJECTS})
set_target_properties(foam4Py_cpp PROPERTIES POSITION_INDEPENDENT_CODE ON)

# Link against dependencies
target_link_libraries(foam4Py_cpp ${FOAM_LIBRARIES})
target_link_libraries(foam4Py_cpp ${Python_LIBRARIES})
target_link_libraries(foam4Py_cpp nlohmann_json::nlohmann_json)

pybind11_add_module(foam4Py_module SHARED foam4Py_cpp_to_py_bindings.C)
target_link_libraries(foam4Py_module PRIVATE foam4Py_cpp)

# Install the library
install(TARGETS foam4Py_cpp
        LIBRARY DESTINATION ${CMAKE_PACKAGE_DIR}/lib
        ARCHIVE DESTINATION ${CMAKE_PACKAGE_DIR}/lib
        #RUNTIME DESTINATION ${CMAKE_PACKAGE_DIR}/bin
        INCLUDES DESTINATION ${CMAKE_PACKAGE_DIR}/include
        )

install(TARGETS foam4Py_module
        LIBRARY DESTINATION ${CMAKE_PACKAGE_DIR}
        ARCHIVE DESTINATION ${CMAKE_PACKAGE_DIR}
        )
