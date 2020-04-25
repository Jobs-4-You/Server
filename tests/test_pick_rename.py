import pytest

from j4u_api.utils.func import pick_rename

test_dict_1 = {"a": {"a1": 1, "a2": 2, "a3": 3,}, "b": 3}

test_dict_2 = {"a": {"a1": 1, "a2": 2, "a3": 3,}, "b": [{"c": 1}, {"c": 2}]}


class TestPickRename:
    def test_nested_pick(self):
        res = pick_rename(test_dict_1, [("aa.jj", "a.a1"), ("ab", "a.a2"), ("bb", "b")])
        print(res)
        print("-" * 100)
