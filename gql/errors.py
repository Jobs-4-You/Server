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


class AuthError(Error):
    def __init__(self, sub_domain, err_msg):
        self.sub_domain = sub_domain
        self.err_msg = err_msg
        super().__init__(100)


class UserNotFound(AuthError):
    def __init__(self, email):
        err_msg = f"Aucun utilisateur avec l'email: {email}"
        super().__init__(1, err_msg)


class InvalidPassword(AuthError):
    def __init__(self, email):
        err_msg = f"Mot de passe invalide pour l'utilisateur: {email}"
        super().__init__(2, err_msg)


class NotAuthenticated(AuthError):
    def __init__(self):
        err_msg = f"Utilisateur non connecte"
        super().__init__(3, err_msg)


class NotAuthorized(AuthError):
    def __init__(self):
        err_msg = f"Utilisateur non autorise"
        super().__init__(4, err_msg)

