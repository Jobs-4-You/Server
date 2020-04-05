from j4u_api.errors.error import Error


class DatabaseError(Error):
    def __init__(self, sub_domain, err_msg):
        super().__init__(300, sub_domain, err_msg)


class NotNullViolation(DatabaseError):
    def __init__(self, column):
        self.column = column
        err_msg = f"{column} ne peut etre null"
        super().__init__(1, err_msg)


class UniqueViolation(DatabaseError):
    def __init__(self, key, value):
        self.key = key
        self.value = value
        err_msg = f"{key}: {value} deja utilise"
        super().__init__(1, err_msg)
