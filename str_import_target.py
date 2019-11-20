from typing import Dict, List

from cmake_generator.cmake_format import cmake_format
from cmake_generator.quote import quote
from cmake_generator.target import ImportTarget, Target

#----------------------------------------------------------------
def str_import_target(
    target      : ImportTarget,
    all_targets : Dict[ str, Target ]
) -> str:

    target_names = ', '.join( [ subtarget for subtarget in target.subtargets ] )
    target_str = cmake_format( """
# ----------------------------------------------------------------
# Import Targets: {SHAKE_CMAKE_GENERATOR_target_names}
""",
    target_names = target_names
    )

    target_str += target.pre_import_inline_cmake
    target_str += cmake_format( """
add_subdirectory( {SHAKE_CMAKE_GENERATOR_src_dir_path} )
""",
       src_dir_path = quote( target.src_dir_path )
    )
    target_str += target.post_import_inline_cmake
    return target_str


