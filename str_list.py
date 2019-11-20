from typing import Any, List

from cmake_generator.cmake_format   import cmake_format
from cmake_generator.quote          import quote

#----------------------------------------------------------------
def python_list_to_cmake_list(
    l : List[ Any ]
) -> str:
    result = '\n'.join( [ str( e ) for e in l ] )
    return result

#----------------------------------------------------------------
def python_list_to_cmake_list_quoted(
    l : List[ Any ]
) -> str:

    quoted_elements = []
    for e in l:
        if e[0] == '$':
            quoted_elements.append( e )
        else:
            quoted_elements.append( quote( e ) )

    result = '\n'.join( quoted_elements )
    return result

#----------------------------------------------------------------
def str_list(
    list_name : str,
    list_value : [ str ]
) -> str:
    set_list_template = 'list( APPEND {SHAKE_CMAKE_GENERATOR_list_name} {SHAKE_CMAKE_GENERATOR_list_value} )'
    set_list_str = cmake_format(
        set_list_template,
        list_name = list_name,
        list_value = python_list_to_cmake_list( list_value )
    )
    return set_list_str