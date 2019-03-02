"""."""
from comp_func import cmp_func

'''
关键点 ：
1. “三点中值”获取好的分割
'''


def key_from_three(sort_nums, left, right, mid):
    """三点中值"""
    left_n, right_n, mid_n = sort_nums[left], sort_nums[right], sort_nums[mid]
    if cmp_func(left_n, right_n):
        if cmp_func(mid_n, left_n):  # mid < left < right
            return left
        if cmp_func(right_n, mid_n):  # left < right < mid
            return right
        return mid  # left < mid < right
    else:
        if cmp_func(mid_n, right_n):  # mid < right < left
            return right
        if cmp_func(left_n, mid_n):  # right < left < mid
            return left
        return mid  # right < mid < left


def partition(sort_nums, left, right, pivot_i, is_descend):
    if left >= right:
        return
    """ 分割数组 """
    s_i = left  # 遍历指针
    p_i = left  # 替换指针
    sort_nums[right], sort_nums[pivot_i] = sort_nums[pivot_i], sort_nums[right]
    pivot_value = sort_nums[right]

    while s_i < right:
        if cmp_func(sort_nums[s_i], pivot_value, is_descend):
            sort_nums[p_i], sort_nums[s_i] = sort_nums[s_i], sort_nums[p_i]
            p_i = p_i + 1
        s_i = s_i + 1

    sort_nums[right], sort_nums[p_i] = sort_nums[p_i], sort_nums[right]
    return p_i


def quick_sort_imp(sort_nums, left, right, is_descend):
    if left >= right:
        return
    pivot_i = key_from_three(sort_nums, left, right, (right-left)//2)
    p_i = partition(sort_nums, left, right, pivot_i, is_descend)
    quick_sort_imp(sort_nums, left, p_i - 1, is_descend)
    quick_sort_imp(sort_nums, p_i + 1, right, is_descend)


def QuickSort(sort_nums, is_descend):
    quick_sort_imp(sort_nums, 0, len(sort_nums) - 1, is_descend)


# TestData = [23, 44, 56, 1, 2, 55, 61, 19, 20, 33, 44, 5, 56, 73, 92, 70]
# print("before_sort: ", TestData)
# QuickSort(TestData, True)
# print("after_sort_descend:  ", TestData)
# QuickSort(TestData, False)
# print("after_sort_not_descend:  ", TestData)
