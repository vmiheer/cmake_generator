from typing import Dict, List

from cmake_generator.str_cmake_config   import str_cmake_config
from cmake_generator.str_import_target  import str_import_target
from cmake_generator.str_new_target     import str_new_target
from cmake_generator.str_project        import str_project, Version
from cmake_generator.str_python_target  import str_python_target
from cmake_generator.target             import ImportTarget, NewTarget, PythonTarget, Target

#----------------------------------------------------------------
class CMakeGenerator:

    def __init__(
        self,
        project_name : str,
        project_version : Version,
        cmake_destination_path : str,
        build_dir : str
    ):
        self.file_writer = open( cmake_destination_path, 'w' )
        self._write( str_cmake_config( build_dir ) )
        self._write( str_project( project_name, project_version ) )


    def __del__( self ):
        self.file_writer.close()


    def _write( self, text : str ) -> None:
        self.file_writer.write( text )


    def _add_target( self, target : Target, all_targets :  Dict[ str, Target ] ) -> None:
        dispatcher = {
            NewTarget       : str_new_target,
            ImportTarget    : str_import_target,
            PythonTarget    : str_python_target
        }
        # we don't write any cmake for header only libraries
        if target.__class__ in dispatcher:
            self._write( dispatcher[ target.__class__ ]( target, all_targets ) )


    def generate( self, target_definitions : List[ Target ] ) -> None:

        target_dictionary = {}
        for target in target_definitions:
                target_dictionary.update( { target.name : target} )

        for target in target_definitions:
            self._add_target( target, target_dictionary )



