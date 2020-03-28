from .error import Error


class TokenError(Error):
    def __init__(self, sub_domain, err_msg):
        self.sub_domain = sub_domain
        self.err_msg = err_msg
        super().__init__(200)


class SessionExpired(TokenError):
    def __init__(self):
        err_msg = f"Votre session a expire, veuillez vous reconnecter"
        super().__init__(1, err_msg)


class InvalidSignupLink(TokenError):
    def __init__(self):
        err_msg = f"Lien d'inscription invalide"
        super().__init__(2, err_msg)


class ExpiredSignupLink(TokenError):
    def __init__(self):
        err_msg = f"Lien d'inscription expiré"
        super().__init__(3, err_msg)


class InvalidVerificationLink(TokenError):
    def __init__(self):
        err_msg = f"Lien de verification de l'email invalide"
        super().__init__(4, err_msg)


class ExpiredVerificationLink(TokenError):
    def __init__(self):
        err_msg = f"Lien de verification de l'email expiré"
        super().__init__(5, err_msg)
