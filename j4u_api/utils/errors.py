import re

from j4u_api.errors.db_errors import NotNullViolation, UniqueViolation


def parse_error_type(err):
    pattern = r"\(psycopg2.errors.(\w*)\)"
    error_type = re.match(pattern, str(err))
    return error_type


def parse_not_null_violation(err):
    pattern = r'null value in column "(\w+)"'
    column = re.match(pattern, str(err.orig)).groups()[0]
    return NotNullViolation(column)


def parse_unique_violation(err):
    pattern = r"\((.*?)\)"
    key, value = re.findall(pattern, str(err.orig))
    return UniqueViolation(key, value)


def parse_db_error(err):
    error_type = parse_error_type(err)
    if error_type is None:
        raise Exception("Internal Server Error")

    error_type = error_type.groups()[0]

    if error_type == "NotNullViolation":
        return parse_not_null_violation(err)
    elif error_type == "UniqueViolation":
        return parse_unique_violation(err)

    else:
        return err

    return 1, 1
