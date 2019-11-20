#----------------------------------------------------------------
def cmake_format(
    string : str,
    **kwargs
) -> str:
    result = string
    for key, value in kwargs.items():
        result = result.replace( '{SHAKE_CMAKE_GENERATOR_' + key + '}', str( value ) )
    return result
