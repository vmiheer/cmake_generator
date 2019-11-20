from enum import auto, Enum

#----------------------------------------------------------------
class TargetType(Enum):
    Executable          = auto()
    HeaderOnlyLibrary   = auto()
    SharedLibrary       = auto()
    StaticLibrary       = auto()