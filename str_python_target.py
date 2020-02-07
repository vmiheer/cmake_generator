from textwrap import indent
from typing import Dict, List

from cmake_generator.cmake_format import cmake_format
from cmake_generator.str_list import python_list_to_cmake_list, python_list_to_cmake_list_quoted
from cmake_generator.str_file import make_glob_expression, str_file_glob_recurse
from cmake_generator.target import Target, HeaderOnlyTarget, NewTarget, ImportTarget, PythonTarget

#----------------------------------------------------------------
def str_python_target(
    target      : PythonTarget,
    all_targets : Dict[ str, Target ]
) -> str:

    target_str = cmake_format( """
# ----------------------------------------------------------------
# Python Target: {SHAKE_CMAKE_GENERATOR_target_name}
""",
       target_name = target.name
    )

    # gob the source files, and add the target
    source_variable_name = target.name + '_glob_files'
    target_str += str_file_glob_recurse( source_variable_name, make_glob_expression( target.src_dir_path ) )
    target_str += _str_add_target( target, source_variable_name )

    # set target properties
    if target.properties:
        for property_name, property_value in target.properties.items():
            target_str += _str_set_target_properties( target.name, property_name, property_value ) + '\n'

    # add include directories of all dependencies
    # but also add a target's own source dir as include dir
    include_dirs = target.include_dirs.copy()
    for dependency_name in target.dependencies:

        if dependency_name not in all_targets:
            raise ValueError( 'Target specification for dependency {} was not found'.format( dependency_name ) )

        dependency = all_targets[ dependency_name ]
        include_dirs.extend( dependency.include_dirs )

    if include_dirs:
        target_str += _str_target_include_directories( target.name, include_dirs )

    if target.dependencies :
        # link all dependency targets
        link_libraries = []
        for dependency_name in target.dependencies:

            if dependency_name not in all_targets:
                raise ValueError( 'Target specification for dependency {} was not found'.format( dependency_name ) )

            dependency = all_targets[ dependency_name ]

            if isinstance( dependency, HeaderOnlyTarget ):
                continue

            if isinstance( dependency, NewTarget ):
                link_libraries.append( dependency.name )
            if isinstance( dependency, ImportTarget ):
                for subtarget in dependency.subtargets:
                    link_libraries.append( subtarget )
            # we don't link header only libraries by name

        if link_libraries:
            target_str += _str_target_link_libraries( target.name, link_libraries )

    target_str += cmake_format( """
set_property( TARGET {SHAKE_CMAKE_GENERATOR_target_name} PROPERTY CXX_STANDARD 17 )    
""",
        target_name = target.name
    )
    return target_str

#----------------------------------------------------------------
def _str_add_target(
    target                  : NewTarget,
    source_variable_name    : str
) -> str:
    add_target_string_template = """
pybind11_add_module( {SHAKE_CMAKE_GENERATOR_target_name} MODULE ${SHAKE_CMAKE_GENERATOR_source_variable_name} )
"""
    return cmake_format(
        add_target_string_template,
        target_name = target.name,
        source_variable_name = '{' + source_variable_name + '}'
    )

#----------------------------------------------------------------
def _str_target_link_libraries(
    target_name     : str,
    library_names   : List[ str ]
):
    link_libraries_template = """
target_link_libraries( {SHAKE_CMAKE_GENERATOR_target_name} PRIVATE 
{SHAKE_CMAKE_GENERATOR_library_names} 
)
"""
    link_libraries_string = cmake_format(
        link_libraries_template,
        target_name     = target_name,
        library_names   = indent( python_list_to_cmake_list( library_names ), '    ' )
    )
    return link_libraries_string

#----------------------------------------------------------------
def _str_set_target_properties(
    target_name     : str,
    property_name   : str,
    property_value  : str
):
    set_target_properties_template = """
set_target_properties( {SHAKE_CMAKE_GENERATOR_target_name} PROPERTIES {SHAKE_CMAKE_GENERATOR_property_name} {SHAKE_CMAKE_GENERATOR_property_value} )
"""
    set_target_properties_str = cmake_format(
        set_target_properties_template,
        target_name     = target_name,
        property_name   = property_name,
        property_value  = property_value
    )
    return set_target_properties_str

#----------------------------------------------------------------
def _str_target_include_directories(
    target_name         : str,
    include_directories : List[ str ]
):
    include_directories_template = """
target_include_directories( {SHAKE_CMAKE_GENERATOR_target_name} PRIVATE 
{SHAKE_CMAKE_GENERATOR_include_directories} 
)
"""
    include_directories_string = cmake_format(
        include_directories_template,
        target_name         = target_name,
        include_directories = indent( python_list_to_cmake_list_quoted( include_directories ), '    ' )
    )
    return include_directories_string