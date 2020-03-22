import graphene
from database.enums import RoleEnum, CiviliteEnum, GroupEnum


RoleEnum = graphene.Enum.from_enum(RoleEnum)
CiviliteEnum = graphene.Enum.from_enum(CiviliteEnum)
GroupEnum = graphene.Enum.from_enum(GroupEnum)
