from cmake_generator.cmake_format import cmake_format
from cmake_generator.quote import quote

#----------------------------------------------------------------
def _str_list_files(
    set_file_template : str,
    file_variable_name : str,
    glob_expression : str
) -> str:
    set_file_str = cmake_format(
        set_file_template,
        file_variable_name = file_variable_name,
        glob_expression = quote( glob_expression )
    )
    return set_file_str

#----------------------------------------------------------------
def make_glob_expression( dir_path : str ):
    return '{}/*'.format( dir_path )

#----------------------------------------------------------------
def str_file_glob_recurse(
    file_variable_name : str,
    glob_expression : str
) -> str:
    set_file_template = """
file( GLOB_RECURSE {SHAKE_CMAKE_GENERATOR_file_variable_name} {SHAKE_CMAKE_GENERATOR_glob_expression} )
"""
    return _str_list_files( set_file_template, file_variable_name, glob_expression )

#----------------------------------------------------------------
def str_file_glob(
    file_variable_name: str,
    glob_expression: str
) -> str:
    set_file_template = """
file( GLOB {SHAKE_CMAKE_GENERATOR_file_variable_name} {SHAKE_CMAKE_GENERATOR_glob_expression} )
"""
    return _str_list_files( set_file_template, file_variable_name, glob_expression )