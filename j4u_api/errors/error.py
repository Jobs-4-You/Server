# Base error class
class Error(Exception):
    def __init__(self, domain, sub_domain, err_msg):
        self.domain = domain
        self.sub_domain = sub_domain
        self.err_msg = err_msg
        super().__init__(self.message)

    @property
    def code(self):
        return self.domain + self.sub_domain

    @property
    def message(self):
        return f"CODE({self.code}) MSG({self.err_msg})"
