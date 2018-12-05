"""."""
import time
# import functools
# @functools.wraps(func)

"""
装饰器
"""


def metric(func):
    """."""
    # 1.可作用于任何函数上，并打印该函数的执行时间
    #
    # 2.能在函数调用的前后打印出'begin call'和'end call'的日志。
    def wrapper(*args, **kw):
        before = time.time()
        print("%s begin call" % (func.__name__))
        ret = func(*args, **kw)
        print("%s end call" % (func.__name__))
        after = time.time()
        use_sec = round(after - before, 2)
        print('%s executed in %s ms' % (func.__name__, use_sec))
        return ret
    return wrapper


def log(text=""):
    """."""
    # 3.既支持 @log ,又支持 @log() ,又支持 @log("execute")
    def wrapper(fn):
        print('%s%s' % (len(text) > 0 and text + " " or text, fn.__name__))
        return fn

    if not isinstance(text, str):
        fn, text = text, ""
        return wrapper(fn)
    else:
        return wrapper

# # 测试


@metric
def fast(x, y):
    """."""
    time.sleep(0.0012)
    return x + y


@metric
def slow(x, y, z):
    """."""
    time.sleep(0.1234)
    return x * y * z


f = fast(11, 22)
s = slow(11, 22, 33)
if f != 33:
    print('测试失败!')
elif s != 7986:
    print('测试失败!')
else:
    print('测试成功!')


@log
def test_metric1():
    """."""
    pass


@log()
def test_metric2():
    """."""
    pass


@log("execute")
def test_metric3():
    """."""
    pass


test_metric1()
test_metric2()
test_metric3()
