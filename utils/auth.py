from gql.errors.auth_errors import NotAuthenticated, NotAuthorized


def jwt_auth_required(func):
    def inner(*args, **kwargs):
        if args[1].context.user is None:
            raise NotAuthenticated().error
        return func(*args, **kwargs)

    return inner


def roles_required(roles):
    def decorator(func):
        def inner(*args, **kwargs):
            user = args[1].context.user
            if user is None:
                raise NotAuthenticated().error
            if user.role in roles:
                return func(*args, **kwargs)
            else:
                raise NotAuthorized().error

        return inner

    return decorator
