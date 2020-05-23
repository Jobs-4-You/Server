from j4u_api.errors.error import Error


class QualtricsError(Error):
    def __init__(self, sub_domain, err_msg):
        super().__init__(400, sub_domain, err_msg)


class ContactAlreadyExists(QualtricsError):
    def __init__(self, email):
        err_msg = f"Contact with {email} already exists"
        super().__init__(1, err_msg)
