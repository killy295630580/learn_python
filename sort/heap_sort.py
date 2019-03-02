"""."""
from comp_func import cmp_func

'''
关键点 ：
1. 构建大顶堆（结果递增） 、小顶堆（结果递减）构建
'''


def filter_down(num_list, count, cur_i, is_descend):
    """将num_list[cur_i]进行下滤 此时堆的边界为count"""
    max_i = 0
    while(True):
        l_child = 2 * cur_i + 1
        r_child = 2 * cur_i + 2
        max_i = cur_i

        if(count > l_child):
            if (not cmp_func(num_list[l_child], num_list[max_i], is_descend)):
                max_i = l_child

        if(count > r_child):
            if(not cmp_func(num_list[r_child], num_list[max_i], is_descend)):
                max_i = r_child

        if(max_i == cur_i):
            break

        num_list[cur_i], num_list[max_i] = num_list[max_i], num_list[cur_i]
        cur_i = max_i


def BuildHeap(num_list, is_descend):
    count = len(num_list)
    if count <= 0:
        return
    cur_index = (count - 1) // 2
    while(cur_index >= 0):
        filter_down(num_list, count, cur_index, is_descend)
        cur_index = cur_index - 1


def HeapSort(sort_nums, is_descend=False):
    count = len(sort_nums)
    if count <= 0:
        return
    BuildHeap(sort_nums, is_descend)
    last_i = count - 1
    while(last_i > 0):
        sort_nums[0], sort_nums[last_i] = sort_nums[last_i], sort_nums[0]
        filter_down(sort_nums, last_i, 0, is_descend)
        last_i = last_i - 1


# TestData = [23, 44, 56, 1, 2, 55, 61, 19, 20, 33, 44, 5, 56, 73, 92, 70]
# print("before_sort: ", TestData)
# HeapSort(TestData)
# print("after_sort_increase:  ", TestData)
# HeapSort(TestData, True)
# print("after_sort_descend:  ", TestData)
