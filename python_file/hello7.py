"""."""


def count(start, end):
    """."""
    def f(i):
        return lambda: i * i
    fs = []
    for i in range(start, end):
        fs.append(f(i))  # f(i)立刻被执行，因此i的当前值被传入f()
    return fs


for f in count(1, 4):
    print(f())


def create_counter():
    """利用闭包返回一个计数器函数，每次调用它返回递增整数."""
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count
    return counter


# # # 测试:
counterA = create_counter()
print(counterA(), counterA(), counterA(), counterA(), counterA())  # 1 2 3 4 5
counterB = create_counter()
if [counterB(), counterB(), counterB(), counterB()] == [1, 2, 3, 4]:
    print('测试通过!')
else:
    print('测试失败!')
