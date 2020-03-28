from graphql import GraphQLError


class Error:
    def __init__(
        self, domain,
    ):
        self.domain = domain

    @property
    def code(self):
        return self.domain + self.sub_domain

    @property
    def message(self):
        return f"CODE({self.code}) MSG({self.err_msg})"

    @property
    def error(self):
        return GraphQLError(self.message)
