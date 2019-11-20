from cmake_generator.cmake_format import cmake_format

#----------------------------------------------------------------
def str_string(
    string_name     : str,
    string_value    : str
) -> str:
    set_string_template = 'string( APPEND {SHAKE_CMAKE_GENERATOR_string_name} {SHAKE_CMAKE_GENERATOR_string_value} )'
    set_string_str = cmake_format(
        set_string_template,
        string_name     = string_name,
        string_value    = string_value
    )
    return set_string_str