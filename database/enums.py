import enum


class RoleEnum(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class CiviliteEnum(enum.Enum):
    M = "M"
    MLLE = "MLLE"
    MME = "MME"


class GroupEnum(enum.Enum):
    COG = "COG"
    CONT = "CONT"
    J4U = "J4U"
    J4UCOG = "J4UCOG"
    NJS = "NJS"
    J4UNJS = "J4UNJS"
