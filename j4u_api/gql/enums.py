import graphene

from j4u_api.database.enums import CiviliteEnum, RoleEnum


def enum_converter(name, enum):
    content = [(e.name, e.value) for e in enum]
    return graphene.Enum(name, content)


RoleEnum = enum_converter("RoleEnumGQL", RoleEnum)
CiviliteEnum = enum_converter("CiviliteEnumGQL", CiviliteEnum)
