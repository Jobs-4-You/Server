import functools
import time

from j4u_api.utils.logging import logger


def _get_path(d, path):
    def f(curr_obj, parts):
        if len(parts) > 1:
            key, remaining_parts = parts[0], parts[1:]
            next_dict = curr_obj.get(key, {})
            next_dict = next_dict if next_dict is not None else {}
            return f(next_dict, remaining_parts)
        elif len(parts) == 1:
            if curr_obj is None:
                from j4u_api.utils.print import pretty_print

                pretty_print(d)
            return curr_obj.get(parts[0])
        else:
            raise Exception("Invalid path parts")

    path_parts = path.split(".")
    return f(d, path_parts)


def _set_path(d, path, value):
    path_parts = path.split(".")
    curr_dict = d
    for part in path_parts[:-1]:
        curr_dict[part] = curr_dict.get(part, {})
        curr_dict = curr_dict[part]
    curr_dict[path_parts[-1]] = value


def pick_rename(d, paths):
    res = {}

    for to_path, from_path in paths:
        value = _get_path(d, from_path)
        _set_path(res, to_path, value)

    return res


def async_timeit(caller_module):
    def _decorate(function):
        @functools.wraps(function)
        async def wrapped_function(*args, **kwargs):
            start = time.time()
            try:
                res = await function(*args, **kwargs)
                return res
            except Exception as err:
                raise err
            finally:
                end = time.time()
                exec_time = end - start
                logger.info(
                    caller_module,
                    function,
                    "Execution time: %f",
                    exec_time,
                    extra={"exec_time": exec_time},
                )

        return wrapped_function

    return _decorate

    return _decorate
