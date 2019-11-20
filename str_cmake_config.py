from cmake_generator.cmake_format import cmake_format
from cmake_generator.quote import quote

#----------------------------------------------------------------
def str_cmake_config(
    out_directory : str
) -> str:

    cmake_config_template = """
# ----------------------------------------------------------------
# This CMake file is generated automatically by the Shake3 CMake Generator
# Don't change this file. Reconfigure the generator instead.

cmake_minimum_required( VERSION 3.12 )

# ----------------------------------------------------------------
# CMake configuration

set( CMAKE_ARCHIVE_OUTPUT_DIRECTORY {SHAKE_CMAKE_GENERATOR_out_directory} )
set( CMAKE_LIBRARY_OUTPUT_DIRECTORY {SHAKE_CMAKE_GENERATOR_out_directory} )
set( CMAKE_RUNTIME_OUTPUT_DIRECTORY {SHAKE_CMAKE_GENERATOR_out_directory} )
set( CMAKE_EXECUTABLE_OUTPUT_PATH   {SHAKE_CMAKE_GENERATOR_out_directory} )

# this option is necessary to automatically export ALL symbols in a library on Windows, 
# without needing to specify __declspec( export ).
# That means it also creates a .lib file for shared libraries
set( CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON )
"""

    cmake_config_string = cmake_format(
        cmake_config_template,
        out_directory = quote( out_directory )
    )

    return cmake_config_string



