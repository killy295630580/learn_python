#### 0. Python 环境变量
变量名|描述
:---|:---
PYTHONPATH		|PYTHONPATH是Python搜索路径，默认我们import的模块都会从PYTHONPATH里面寻找。
PYTHONSTARTUP 	|Python启动后，先寻找PYTHONSTARTUP环境变量，然后执行此变量指定的文件中的代码。
PYTHONHOME 		|另一种模块搜索路径。它通常内嵌于的PYTHONSTARTUP或PYTHONPATH目录中，使得两个模块库更容易切换。
PYTHONCASEOK 	|加入PYTHONCASEOK的环境变量, 就会使python导入模块的时候不区分大小写.
#### 1. 通过缩进确定作用域
#### 2. lambda 函数 ：  lambda 参数:return 结果
#### 3. 比较运算符 ：
符号|作用
:---|:---
\>			|大于
<				|小于
==			|等于
\>=			|大于等于
<=			|小于等于
not 			|否
in			|包含
not in		|不包含
is			|相同
is not		|不相同

#### 4. 数据结构类型
	- 字典dict  -> {}  : 有键值对
	- 集合set   -> {,} ：无键值对
	- 元组tuple -> ()  ：不可变
	- 列表list  -> []  ：可变
	- 切片             ：[开始Index(忽略则表头) : 结束Index(忽略则表尾) : 步长(忽略则1)] ， 返回一个新的元组(列表)

	- 各类推导式 -> 返回一个列表
	  [(结果表达式) for循环1 for循环2 if表达式1 if表达式2 ...]

	- 生成器 -> 返回一个生成器generator
	 ((结果表达式) for循环1 for循环2 if表达式1 if表达式2 ...)
	 只要函数中包含yield关键字, 则会形成一个生成器, 遇到yield语句返回, 再次执行就会从上次返回的yield语句处继续执行

	以上4种集合、生成器、字符串 ， 统称 可迭代对象: Iterable ， 可用于for循环
	另外，生成器 可通过next()获得下一项 ，称作迭代器Iterator

	而可迭代的对象Iterable , 可使用 iter(对象) 函数，转化为迭代器Iterator
	可使用 isinstance(对象, Iterable) 检测对象是否可迭代对象
	可使用 isinstance(对象, Iterator) 检测对象是否迭代器

#### 5. 高阶函数： 参数是函数的函数
	map(func,list)			  : 将func依次作用到序列的每个元素 ， 返回生成列表的迭代器
	filter(func,list)		  : 将func依次作用到序列的每个元素 ， Func返回True保留该元素, 返回False则丢弃， 最终返回生成列表的迭代器
	reduce(func,list)		  : 从列表第一个元素开始, 把结果继续和序列的下一个元素做累积计算, 返回最终结果
	sorted(list,list_func,is_reverse) : 队列表进行排序 ， 第二个参数作用于列表的每一个元素 ， 第三个元素决定是否逆序， 返回排序结果

#### 6.获取对象信息
	type(对象) : 可以获得对象的类型
	另外，types模块中定义了一些常量 ， 可以用于表示对象的类型
	例如 ： 
	type(函数名)        ==  types.FunctionType
	type(内置函数)      ==  types.BuiltinFunctionType
	type(lambda式函数)  ==  types.LambdaType
	type(生成器)        ==  types.GeneratorType

#### 7.判断对象类型
	isinstance(对象, 判断的类型) : 判断对象是否指定的类型,可用于判断父类
	isinstance(对象, (判断的类型1, 判断的类型2))  : 判断对象是否指定的类型列表中的一个

#### 8.对象的属性和方法
	dir(对象) ：获得一个对象的所有属性和方法
	hasattr(对象, 属性名) ： 判断对象是否拥有指定属性或方法
	setattr(对象, 属性名) ： 设置对象中的指定属性或方法
	getattr(对象, 属性名) ： 获取对象中的指定属性或方法, 如果没有 ， 则会抛出AttributeError
	getattr(对象, 属性名, 默认值) ： 获取对象中的指定属性或方法, 如果没有，则返回默认值

#### 9. 类方法跟普通函数的区别
	- 类方法的第一个参数必须是指向类对象的一个指针， 但是调用时不需要传此参数 ， 因为类方法调用时会自动赋值上
	- 普通函数则没有此规定

#### 10. 类属性 和 实例属性
	-- 类属性是该类自身的属性 ， 是一个可供实例化该类的所有的实例共同使用的属性
	-- 实例属性是实例自己拥有的属性 ， 不能被别的实例所使用 ， 即便是同一个类型的实例 ， 只针对本身有效 ， 互不干扰
	-- 实例属性 尽量不要跟 类属性 起相同名字 ， 否则类属性会被屏蔽掉

#### 11. 类中有特殊用途的属性与函数
	__slots__      : 在类定义的时候添加此属性，用于限制实例只能添加列表中的属性。子类无效。
	__init__(self) : 类的构造函数
	__len__(self)  : 让类能使用len()函数
	__str__(self)  : 定义类被print时打印出来的内容
	__repr__(self) : 定义类被直接显示时打印出来的内容
	__iter__(self) : 让类具有类似list或tuple那样被迭代的功能, 返回一个可迭代对象
	__next__(self) : 定义可迭代对象 ， 被next()调用
	__getitem__(self,index) : 定义[index]操作符"读"功能，
				: 如果index为slice类型，即可以定义切片操作
	__setitem__(self,index) ：定义[index]操作符"写"功能
	__delitem__(self,index) ：定义del[index]操作
	__getattr__(self,attr)	: 用于调用的属性或者方法不存在时被调用
	__call__(self,args)	: 让类对象能像函数一样被调用 , 可通过callable(对象)判断此方法有没有被定义
	...... 
[官方文档]:https://docs.python.org/3/reference/datamodel.html#special-method-names
[Python的官方文档][官方文档]

#### 12. 装饰器 @property
[函数装饰器]:python_file\hello9.py
[类装饰器]:python_file\hello12.py
[函数的装饰器][函数装饰器]
[类的装饰器][类装饰器]

#### 13.













-----
[1]:http://www.runoob.com/python3/python3-tutorial.html
[2]:http://www.runoob.com/manual/pythontutorial3/docs/html/appetite.html
[3]:https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000
##### [Python 3 教程][1]
##### [Python 入门指南][2]
##### [廖雪峰的Python教程][3]

