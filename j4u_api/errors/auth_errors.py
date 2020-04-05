from j4u_api.errors.error import Error


class AuthError(Error):
    def __init__(self, sub_domain, err_msg):
        super().__init__(100, sub_domain, err_msg)


class UserNotFound(AuthError):
    def __init__(self, email):
        self.mail = email
        err_msg = f"Aucun utilisateur avec l'email: {email}"
        super().__init__(1, err_msg)


class InvalidPassword(AuthError):
    def __init__(self, email):
        self.mail = email
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
