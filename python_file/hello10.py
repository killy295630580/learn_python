"""."""
# 偏函数
# functools.partial
# functools.partial(原函数，需要固定的参数以及初始值)

import functools


def list_add(a, b, c, d):
    """."""
    print(a + b + c + d)


list_add2 = functools.partial(list_add, d=10)
list_add3 = functools.partial(list_add, d=11)

list_add(1, 2, 3, 4)
# 10
list_add2(1, 2, 3)
# 16
list_add3(1, 2, 3, d=5)
# 11
list_add3(1, 2, 3)
# 17
