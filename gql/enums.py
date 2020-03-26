import graphene
from database.enums import RoleEnum, CiviliteEnum, GroupEnum


def enum_converter(name, enum):
    content = [(e.name, e.value) for e in enum]
    return graphene.Enum(name, content)


RoleEnum = enum_converter("RoleEnumGQL", RoleEnum)
CiviliteEnum = enum_converter("CiviliteEnumGQL", CiviliteEnum)
GroupEnum = enum_converter("GroupEnumGQL", GroupEnum)
