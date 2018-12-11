"""."""
from functools import reduce


def prod(L):
	"""."""
    return reduce((lambda x, y: x*y), L)


print('3 * 5 * 7 * 9 =', prod([3, 5, 7, 9]))
if prod([3, 5, 7, 9]) == 945:
    print('测试成功!')
else:
    print('测试失败!')


DigitalList = {
    "0": 0, "1": 1, "2": 2,
    "3": 3, "4": 4, "5": 5,
    "6": 6, "7": 7, "8": 8,
    "9": 9, ".": -1}


def str2float_1(s):
    dig_list = s.split(".")
    if len(dig_list) != 2:
        return 0
    dig_list[0] = len(dig_list[0]) <= 0 and dig_list[0] or "0"

    def map_func(ch): return DigitalList[ch]

    def reduce_func(x, y): return x * 10 + y

    part1 = reduce(reduce_func, map(map_func, dig_list[0]))
    part2 = reduce(reduce_func, map(
        map_func, dig_list[1])) * 0.1 ** len(dig_list[1])

    return part1 + part2


DigitalList = {
    "0": 0, "1": 1, "2": 2,
    "3": 3, "4": 4, "5": 5,
    "6": 6, "7": 7, "8": 8,
    "9": 9, ".": -1}


def str2float(s):
    has_point = False
    point_count = 10

    def reduce_add(x, y):
        nonlocal has_point
        nonlocal point_count
        if x < 0 or y < 0:
            has_point = True
        ret_num = x > 0 and x or 0

        if y >= 0:
            if has_point:
                ret_num = ret_num + y / point_count
                point_count *= 10
            else:
                ret_num = ret_num * 10 + y

        return ret_num

    return reduce(reduce_add, list(map((lambda x: DigitalList[x]), s)))


print('str2float(\'10.456\') =', str2float('10.456'))
if abs(str2float('10.456') - 10.456) < 0.00001:
    print('测试成功!')
else:
    print('测试失败!')
