"""."""
from comp_func import cmp_func

'''
关键点 ：
1. 从指定坐标往回寻找符合条件的位置
'''


def InsertSort(sort_nums, is_descend=False):
    count = len(sort_nums)
    cur_i = 1
    while cur_i < count:
        find_i = cur_i - 1
        temp = sort_nums[cur_i]
        while find_i >= 0:
            if not cmp_func(sort_nums[find_i], temp, is_descend):
                sort_nums[find_i + 1] = sort_nums[find_i]
                find_i = find_i - 1
            else:
                break
        sort_nums[find_i + 1] = temp
        cur_i = cur_i + 1


# TestData = [23, 44, 56, 1, 2, 55, 61, 19, 20, 33, 44, 5, 56, 73, 92, 70]
# print("before_sort: ", TestData)
# InsertSort(TestData)
# print("after_sort_increase:  ", TestData)
# InsertSort(TestData, True)
# print("after_sort_descend:  ", TestData)
