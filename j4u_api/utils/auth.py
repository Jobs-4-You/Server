from j4u_api.errors.auth_errors import NotAuthenticated, NotAuthorized


def jwt_auth_required(func):
    def inner(*args, **kwargs):
        if args[1].context.user is None:
            raise NotAuthenticated()
        return func(*args, **kwargs)

    return inner


def roles_required(roles):
    def decorator(func):
        def inner(*args, **kwargs):
            user = args[1].context.user
            if user is None:
                raise NotAuthenticated()
            if user.role in roles:
                return func(*args, **kwargs)
            else:
                raise NotAuthorized()

        return inner

    return decorator
