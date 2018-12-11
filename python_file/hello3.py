"""."""
# -*- coding: utf-8 -*-


def triangles():
    """."""
    list_temp = [1]
    while True:
        yield list_temp
        length = len(list_temp)
        list_temp = [list_temp[i] + list_temp[i + 1]
                     for i in range(length) if i + 1 < length]
        list_temp.insert(0, 1)
        list_temp.append(1)
        list_temp = list_temp


def triangles1():
    """."""
    list_temp = [1]
    while True:
        yield list_temp
        list_temp = [list_temp[i] + list_temp[i + 1]
                     for i in range(len(list_temp) - 1)]
        list_temp.insert(0, 1)
        list_temp.append(1)

# 期待输出:
# [1]
# [1, 1]
# [1, 2, 1]
# [1, 3, 3, 1]
# [1, 4, 6, 4, 1]
# [1, 5, 10, 10, 5, 1]
# [1, 6, 15, 20, 15, 6, 1]
# [1, 7, 21, 35, 35, 21, 7, 1]
# [1, 8, 28, 56, 70, 56, 28, 8, 1]
# [1, 9, 36, 84, 126, 126, 84, 36, 9, 1]


# 以下是测试代码
n = 0
results = []
for t in triangles():
    print(t)
    results.append(t)
    n = n + 1
    if n == 10:
        break
if results == [
    [1],
    [1, 1],
    [1, 2, 1],
    [1, 3, 3, 1],
    [1, 4, 6, 4, 1],
    [1, 5, 10, 10, 5, 1],
    [1, 6, 15, 20, 15, 6, 1],
    [1, 7, 21, 35, 35, 21, 7, 1],
    [1, 8, 28, 56, 70, 56, 28, 8, 1],
    [1, 9, 36, 84, 126, 126, 84, 36, 9, 1]
]:
    print('测试通过!')
else:
    print('测试失败!')
    print(results)
