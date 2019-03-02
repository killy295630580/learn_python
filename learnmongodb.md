
## 简介
----------------------------------------------------------------------
MongoDB 特性 | 优势
:---|:---
事务支持 | MongoDB 目前只支持单文档事务，需要复杂事务支持的场景暂时不适合
灵活的文档模型 | JSON 格式存储最接近真实对象模型，对开发者友好，方便快速开发迭代
高可用复制集 | 满足数据高可靠、服务高可用的需求，运维简单，故障自动切换
可扩展分片集群 | 海量数据存储，服务能力水平扩展
高性能 | mmapv1、wiredtiger、mongorocks（rocksdb）、in-memory 等多引擎支持满足各种场景需求
强大的索引支持 | 地理位置索引可用于构建 各种 O2O 应用、文本索引解决搜索的需求、TTL索引解决历史数据自动过期的需求
Gridfs | 解决文件存储的需求
aggregation & mapreduce | 解决数据分析场景需求，用户可以自己写查询语句或脚本，将请求都分发到 MongoDB 上完成

- **适用于：**
- 网站数据：Mongo 非常适合实时的插入，更新与查询，并具备网站实时数据存储所需的复制及高度伸缩性。
- 缓存：由于性能很高，Mongo 也适合作为信息基础设施的缓存层。在系统重启之后，由Mongo 搭建的持久化缓存层可以避免下层的数据源过载。
- 大尺寸、低价值的数据：使用传统的关系型数据库存储一些数据时可能会比较昂贵，在此之前，很多时候程序员往往会选择传统的文件进行存储。
- 高伸缩性的场景：Mongo 非常适合由数十或数百台服务器组成的数据库，Mongo 的路线图中已经包含对MapReduce 引擎的内置支持。
- 用于对象及JSON 数据的存储：Mongo 的BSON 数据格式非常适合文档化格式的存储及查询。
+ **不适用于：**
+ 高度事务性的系统：例如，银行或会计系统。传统的关系型数据库目前还是更适用于需要大量原子性复杂事务的应用程序。
+ 传统的商业智能应用：针对特定问题的BI 数据库会产生高度优化的查询方式。对于此类应用，数据仓库可能是更合适的选择。
+ 需要SQL 的问题。


SQL术语/概念 | MongoDB术语/概念 | 解释/说明
:---|:---|:---
database | database | 数据库
table | collection | 数据库表/集合
row | document | 数据记录行/文档
column | field | 数据字段/域
index | index | 索引
table joins	 | | 表连接,MongoDB不支持
primary key	| primary key | 主键,MongoDB自动将_id字段设置为主键
- MongoDB 的主要目标是在键/值存储方式（高性能和高度伸缩性）和传统的RDBMS 系统（丰富的功能）之间架起一座桥梁，它集两者的优势于一身。


## 0. windows下安装、卸载
----------------------------------------------------------------------

+ 官网下载 ：https://www.mongodb.com/ , 安装。
  - 建议把 bin 目录加到系统的路径 path。
+ 创建存储数据库的文件夹。假设：D:/mongodb/data
+ 通过普通启动:  （不需要使用管理员模式打开命令行）
  - mongod.exe --dbpath D:/mongodb/data
  - 默认的端口是27017
  - 连接服务: mongo.exe
  - **卸载：** 只需要关闭命令行，并且直接删除安装目录

+ 通过Mongodb安装到**系统服务**:  （使用**管理员模式**打开命令行）
  - 创建一个log文件. 假设：D:/mongodb/log/mongo.log，内容为空。
  - 创建一个配置文件. 假设：D:/mongodb/mongod.cfg , 内容如下：
```
systemLog:
    destination: file
    path: "d:\\mongodb\\log\\mongo.log"
    logAppend: true
storage:
    dbPath: "d:\\mongodb\\data"
net:
    bindIp: 127.0.0.1
    port: 27017
```
  - 把mongodb服务安装到系统服务： mongod --config "d:/mongodb/mongod.cfg" --install
  - 查询windows的系统服务，确保可以找到MongoDB的一个服务。
  - 启动Mongodb的服务 ： net start MongoDB
+ 卸载流程：（使用**管理员模式**打开命令行）
  - 停止Mongodb的服务 ： net stop MongoDB
  - 从系统服务删除mongodb服务 ： mongod --remove
  - 查询windows的系统服务，确保MongoDB服务已经被删除
  - 删除安装目录。


## 1.MongoDB 连接
----------------------------------------------------------------------

标准 URI 连接语法：
`mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]`

+ <u>**mongodb://**</u> 这是固定的格式，必须要指定。
+ <u>**username:password@**</u> 可选项，如果设置，在连接数据库服务器之后，驱动都会尝试登陆这个数据库
+ <u>**host1**</u> 必须的指定至少一个host, host1 是这个URI唯一要填写的。它指定了要连接服务器的地址。如果要连接复制集，请指定多个主机地址。
+ <u>**portX**</u> 可选的指定端口，如果不填，默认为27017
+ <u>**/database**</u> 如果指定username:password@，连接并验证登陆指定数据库。若不指定，默认打开 test 数据库。
+ <u>**?options**</u> 是连接选项。如果不使用/database，则前面需要加上/。所有连接选项都是键值对name=value，键值对之间通过&或;（分号）隔开

其中，选项如下：
选项 | 描述
--- |:---
replicaSet=name | 验证replica set的名称。 Impliesconnect=replicaSet.
slaveOk=true\|false | **true:** 在connect=direct模式下，驱动会连接第一台机器，即使这台服务器不是主。<br>在connect=replicaSet模式下，驱动会发送所有的写请求到主服务器，并且把读取操作分布在其他从服务器。<br>**false:** 在 connect=direct模式下，驱动会自动找寻主服务器。<br>在connect=replicaSet 模式下，驱动仅仅连接主服务器，并且所有的读写命令都连接到主服务器。
connectTimeoutMS=ms | 可以打开连接的时间。
socketTimeoutMS=ms | 发送和接受sockets的时间。
safe=true\|false | **true:** 在执行更新操作之后，驱动都会发送getLastError命令来确保更新成功。(还要参考 wtimeoutMS). <br>**false:** 在每次更新之后，驱动不会发送getLastError来确保更新成功。
fsync=true\|false | **true:** 驱动添加 { fsync : true } 到 getlasterror 命令.**应用于 safe=true**.<br>**false:** 驱动不会添加到getLastError命令中。
w=n | 驱动添加 { w : n } 到getLastError命令. **应用于 safe=true**。
wtimeoutMS=ms | 驱动添加 { wtimeout : ms } 到 getlasterror 命令. **应用于 safe=true**.
journal=true\|false | 如果设置为 true, 同步到 journal (在提交到数据库前写入到实体中). **应用于 safe=true**.


### 数据库连接实例：
----------------------------------------------------------------------
通过 shell 连接 MongoDB 服务：
>`$ ./mongo`

连接本地数据库服务器，端口是默认的。
>`mongodb://localhost`

使用用户名fred，密码foobar登录localhost的admin数据库。
>`mongodb://fred:foobar@localhost`

使用用户名fred，密码foobar登录localhost的baz数据库。
>`mongodb://fred:foobar@localhost/baz`

连接 replica pair, 服务器1为example1.com服务器2为example2。
>`mongodb://example1.com:27017,example2.com:27017`

连接 replica set 三台服务器 (端口 27017, 27018, 和27019):
>`mongodb://localhost,localhost:27018,localhost:27019`

连接 replica set 三台服务器, 写入操作应用在主服务器 并且分布查询到从服务器。
>`mongodb://host1,host2,host3/?slaveOk=true`

直接连接第一个服务器，无论是replica set一部分或者主服务器或者从服务器。
>`mongodb://host1,host2,host3/?connect=direct;slaveOk=true`

当你的连接服务器有优先级，还需要列出所有服务器，你可以使用上述连接方式。

安全模式连接到localhost: 
>`mongodb://localhost/?safe=true`

以安全模式连接到replica set，并且等待至少两个复制服务器成功写入，超时时间设置为2秒。
>`mongodb://host1,host2,host3/?safe=true;w=2;wtimeoutMS=2000`


## 2. 数据库
----------------------------------------------------------------------

+ 一个mongodb中可以建立多个数据库。
+ MongoDB的默认数据库为"db"，该数据库存储在data目录中。
+ MongoDB的单个实例可以容纳多个独立的数据库，每一个都有自己的集合和权限，不同的数据库也放置在不同的文件中。
+ 如果你插入数据时没有创建新的数据库，集合将存放在默认数据库中。

命令 | 作用
:---|:---
db | 显示当前数据库对象。
use xxx | 连接到一个指定的数据库。如果数据库不存在，则**创建数据库**。
show dbs | 显示所有数据的列表。
show tables | 显示当前数据库的所有的集合。
show collections | 查看已有集合。

+ 刚创建的数据库并不会在数据库的 **show dbs** 列表中， 要显示它，我们需要向数据库中插入一些数据。
+ 集合只有在内容插入后才会创建!  就是说，创建集合(数据表)后要再插入一个文档(记录)，集合才会真正创建。

数据库名命名规范：
+ UTF-8字符串。
+ 不能是空字符串（"")。
+ 不得含有' '（空格)、.、$、/、\和\0 (空字符)。
+ 应全部小写。
+ 最多64字节。

另外，有一些数据库名是保留的，可以直接访问这些有特殊作用的数据库。
+ **admin:** 从权限的角度来看，这是"root"数据库。要是将一个用户添加到这个数据库，这个用户自动继承所有数据库的权限。一些特定的服务器端命令也只能从这个数据库运行，比如列出所有的数据库或者关闭服务器。
+ **local:** 这个数据永远不会被复制，可以用来存储限于本地单台服务器的任意集合
+ **config:** 当Mongo用于分片设置时，config数据库在内部使用，用于保存分片的相关信息。


## 3. 集合
----------------------------------------------------------------------

+ 集合就是 MongoDB 文档组，类似于 RDBMS （关系数据库管理系统：Relational Database Management System)中的表格。
+ 集合没有固定的结构，对集合可以插入不同格式和类型的数据。
+ 当第一个文档插入时，集合就会被创建。

集合名命名规范：
+ 集合名不能是空字符串 **""**。
+ 集合名不能含有 **\0** 字符（空字符)，这个字符表示集合名的结尾。
+ 集合名不能以" **system.** "开头，这是为系统集合保留的前缀。
+ 用户创建的集合名字不能含有保留字符。有些驱动程序的确支持在集合名里面包含，这是因为某些系统生成的集合中包含该字符。除非你要访问这种系统创建的集合，否则千万不要在名字里出现 **$**。　


## 4.元数据
----------------------------------------------------------------------

+ 数据库的信息是存储在集合中。
+ 使用了系统的命名空间 ： **\<dbname>.system.*** ，其是一个包含多种系统信息的特殊集合(Collection)。

集合命名空间 | 描述
:----|:----
\<dbname>.system.namespaces | 列出所有名字空间。
\<dbname>.system.indexes | 列出所有索引。
\<dbname>.system.profile | 包含数据库概要(profile)信息。
\<dbname>.system.users | 列出所有可访问数据库的用户。
\<dbname>.local.sources | 包含复制对端（slave）的服务器信息和状态。

+ 在 **system.indexes** 插入数据，可以创建索引。
	但除此之外该表信息是不可变的(特殊的drop index命令将自动更新相关信息)。
+ **system.users** 是可修改的。 
+ **system.profile** 是可删除的。


## 5. 文档
----------------------------------------------------------------------

+ 文档是一组键值(key-value)对。（BSON）
+ 文档中的键/值对是有序的。
+ 文档中的值不仅可以是在双引号里面的字符串，还可以是其他几种数据类型（甚至可以是整个嵌入的文档)，不需要相同的数据类型。
+ MongoDB区分类型和大小写。
+ MongoDB的文档不能有重复的键。
+ 文档的键是字符串。除了少数例外情况，键可以使用任意UTF-8字符。
+ **主键** (MongoDB 提供了 key 为 _id )

文档键命名规范：
+ 键不能含有\0 (空字符)。这个字符用来表示键的结尾。
+ **.** 和 **$** 有特别的意义，只有在特定环境下才能使用。
+ 下划线"_"开头的键是保留的(不是严格要求的)。


## 6.MongoDB 数据类型
----------------------------------------------------------------------

数据类型 | 描述
:----|:----
String | 字符串。存储数据常用的数据类型。只有 **UTF-8 编码** 的字符串才是合法的。
Integer | 整型数值。根据你所采用的服务器，可分为 32 位或 64 位。
Boolean | 布尔值。
Double | 双精度浮点值。
Min/Max keys | 将一个值与 BSON（二进制的 JSON）元素的最低值和最高值相对比。
Array | 用于将数组或列表或多个值存储为一个键。
Timestamp | 时间戳。记录文档修改或添加的具体时间。时间戳值是一个 64 位的值。
Object | 用于内嵌文档。
Null | 用于创建空值。
Symbol | 符号。该数据类型基本上等同于字符串类型，但不同的是，它一般用于采用特殊符号类型的语言。
Date | 日期时间。用 UNIX 时间格式来存储当前日期或时间。你可以指定自己的日期时间：创建 Date 对象，传入年月日信息。
Object ID | 对象 ID。类似唯一主键，可以很快的去生成和排序，包含 12 bytes。**文档** 必须有一个 _id 键
Binary Data | 二进制数据。
Code | 代码类型。用于在文档中存储 JavaScript 代码。
Regular expression | 正则表达式类型。

**ObjectId：** 一个**12字节** BSON 类型数据
+ 前4个字节表示时间戳
+ 接下来的3个字节是机器标识码
+ 紧接的两个字节由进程id组成（PID）
+ 最后三个字节是随机数。
- 创建新的ObjectId
`ObjectId()`
- 文档的时间戳
`ObjectId("5349b4ddd2781d08c09890f4").getTimestamp()`
- 转换为字符串
`ObjectId("5349b4ddd2781d08c09890f4").str`


## 7.MongoDB 删除
----------------------------------------------------------------------

+ 删除数据库
`db.dropDatabase()`
+ 删除集合
`db.collection.drop()`
+ 删除文档
```
db.collection.remove(
   <query>, // 可选，删除的文档的条件。
   {
     justOne: <boolean>, //可选，默认值 false。如果设为 true 或 1，则只删除一个文档，如果设为 false 或 不设置，则删除所有匹配条件的文档。
     writeConcern: <document> //（可选）抛出异常的级别。
   }
)
或
db.collection.remove(<query>,justOne) // justOne 默认为 false。


db.collection.remove({}) //删除集合中所有文档
```


## 8.MongoDB 创建集合
----------------------------------------------------------------------

+ 在 MongoDB 中，你不需要创建集合。当你插入一些文档时，MongoDB 会自动创建集合。
  `db.mycol1.insert({"name" : "XXXX"}) // 创建了集合 mycol1 ，并且插入了一份数据`

+ 手动创建集合
	`db.createCollection(name, options)`
	**name:** 要创建的集合名称
	**options:** 可选参数, 指定有关内存大小及索引的选项，使用花括号{}包住。

options字段 | 类型 | 描述
:----|:----|:----
capped | 布尔 |(可选)如果为 true，则创建固定集合。<br>固定集合是指有着固定大小的集合，当达到最大值时，它会自动覆盖最早的文档。<br>**当该值为 true 时，必须指定 size 字段。**
size | 数值 |(可选)为固定集合指定一个最大值（以字节计）。<br>**如果 capped 为 true，必须指定此字段。**
max | 数值 |(可选)指定固定集合中包含文档的最大数量。
autoIndexId | 布尔 |(可选)如为 true，自动在 _id 字段创建索引。默认为 false。

**capped collections：** 固定集合
+ Capped collections 就是**按照插入顺序储存**的**固定大小**的collection。
+ 性能出色、环形列队、队列过期。 
+ 能插入、能更新，但是更新不能超出固定大小，否则更新失败。
+ 不允许删除文档，需要使用 drop() 方法一次性删除所有的文档，并且drop后，必须显式的重新创建这个集合。
- 用法1:储存日志信息
- 用法2:缓存一些少量的文档
```
\\创建
db.createCollection("mycol2", 
{
  capped:true, 
  size:100000,  // 固定大小(字节)
  max:1000      // 文档个数(个)
})
\\判断是否固定集合
db.cappedLogCollection.isCapped()
\\转换为固定集合
db.runCommand({"convertToCapped":"posts",size:10000})
```

## 9.MongoDB 插入文档
----------------------------------------------------------------------

语法：
`db.COLLECTION_NAME.insert({document})`
+ 如果集合COLLECTION_NAME不在该数据库中， MongoDB 会自动创建该集合并往里面插入文档。

`var doc = {document}`
`db.COLLECTION_NAME.insert(doc)`
+ 也可以将{document}保存为变量，再进行插入操作

`db.collection.insertOne({"a": 3})`
+ 插入一条文档数据

`db.collection.insertMany([{"b": 3}, {'c': 4}])`
+ 插入若干条文档数据


## 10.MongoDB 更新文档
----------------------------------------------------------------------

+ update()
```
db.collection.update(
   <query>, //update的查询条件，类似sql update查询内where后面的。 
   <update>, // update的对象和一些更新的操作符（如$,$inc...）等，类似sql update查询内set后面的
   {
     upsert: <boolean>,//可选，默认false。如果不存在update的记录，是否插入objNew，true为插入，false为不插入。
     multi: <boolean>,//可选，默认false。true：就把按条件查出来多条记录全部更新,false：只更新找到的第一条记录。
     writeConcern: <document> //可选，抛出异常的级别。
   }
)
同样支持下面的格式：
db.collection.update(<query>,<update>,upsert,multi)
```
+ save()
 	如果 document参数 中不指定 _id 字段, save() 方法类似于 insert() 方法。
 	如果 document参数 中指定 _id 字段，则会更新该 _id 文档的数据。
```
db.collection.save(
   <document>,//文档数据。
   {
     writeConcern: <document> //可选，抛出异常的级别。
   }
)
```
+ 更新文档中的数据应当使用**原子操作**，替换整个文档则不需要。
+ **实例：** 
只更新第一条记录：
`db.col.update( { "count" : { $gt : 1 } } , { $set : { "test2" : "OK"} } );`
全部更新：
`db.col.update( { "count" : { $gt : 3 } } , { $set : { "test2" : "OK"} },false,true );`
只添加第一条：
`db.col.update( { "count" : { $gt : 4 } } , { $set : { "test5" : "OK"} },true,false );`
全部添加进去:
`db.col.update( { "count" : { $gt : 5 } } , { $set : { "test5" : "OK"} },true,true );`
全部更新：
`db.col.update( { "count" : { $gt : 15 } } , { $inc : { "count" : 1} },false,true );`
只更新第一条记录：
`db.col.update( { "count" : { $gt : 10 } } , { $inc : { "count" : 1} },false,false );`

**定位符$：**
+ 定位符$用于确定数组中的一个要被更新的元素的位置，而不须使用具体指定该元素在数组中的位置。
```
// 更新数组中的值
{"<array>.$": value}
// 更新数组中的文档 
db.collection.update(
   { <query selector> },
   { <update operator>: { "array.$.field" : value } }
)
```

**原子操作**常用命令：
----------------------------------------------------------------------
**\$set:**
> 用来指定一个键并更新键值，若键不存在并创建。
> { \$set : { field : value } }

**\$unset:**
> 用来删除一个键。
> { \$unset : { field : 1} }

**\$inc:**
> 可以对文档的某个值为数字型（只能为满足要求的数字）的键进行增减的操作。
> { \$inc : { field : value } }

**\$push:**
> 把value追加到**数组**field里面去，如果field不存在，会新增一个数组类型加进去。
> { \$push : { field : value } }

**\$pushAll:**
> 同\$push,只是一次可以追加多个值到一个数组字段内。
> { \$pushAll : { field : value_array } }

**\$pull:**
> 从**数组**field内删除一个等于value值。
> { \$pull : { field : _value } }

**\$addToSet:**
> 增加一个值到**数组**field内，而且只有当这个值不在数组内才增加。
> { \$addToSet : { field : value } }

**\$pop:**
> 删除数组的第一个1或最后一个元素-1
> { \$pop : { field : 1 } }

**\$rename:**
> 修改字段名称
> { \$rename : { old_field_name : new_field_name } }

**\$bit:**
> 位操作，integer类型
> {$bit : { field : {and : 5}}}

偏移操作符 （*）

## 11.MongoDB 查询文档
----------------------------------------------------------------------
```
db.collection.find(
	query, // 查询条件， (可选，使用查询操作符指定查询条件)
	projection // 投影条件， (可选，使用投影操作符指定返回的键。 Key设置为1用于显示字段，而0用于隐藏字段。)
)

db.col.find().pretty() //以格式化的方式来显示所有文档
```
**AND 条件** :  传入多个条件，以**逗号**隔开,或使用关键字 **\$and**
>db.col.find({key1:value1 **,** key2:value2}).pretty()
>db.col.find({**\$and:[**{key1: value1}, {key2:value2} **]**}).pretty()

**OR  条件** : 使用关键字 **\$or**
>db.col.find({**\$or:[**{key1: value1}, {key2:value2} **]**}).pretty()

**AND 和 OR 可联合使用**: 
>db.col.find({"likes": {\$gt:50}**,** **\$or:[**{"by": "菜鸟教程"},{"title": "MongoDB 教程"}**]**}).pretty()
>db.col.find({**\$and:[** { "likes": {\$gt:50} } , { **\$or:[**{"by": "菜鸟教程"} , {"title": "MongoDB 教程"} **]** } **]**}).pretty()

**字段嵌套子集合**
>db.col.find({**"key.子Key"**:value}).pretty()

**投影操作（指定字段）：** 限制字段显示or隐藏。1用于显示该字段，而0用于隐藏该字段。
> "_id" 默认为 1， 隐藏需要手动设为 0。
> db.collection.find({}, **{KEY:1}** )



## 12.MongoDB 条件操作符 **`{ <字段名>: { <操作符>: <比较值> }, ... }`**
----------------------------------------------------------------------

+ 等于：
>MongoDB ： db.collection.find({ price **:** 100 })
>RDBMS ： where likes == 100
+ 不等于：**\$ne**  
>MongoDB ： db.collection.find({ price:{ **\$ne:** 100 }})
>RDBMS ： where likes != 100
+ 大于： **\$gt**  
>MongoDB ： db.collection.find({ price:{ **\$gt:** 100 }})
>RDBMS ： where likes < 100
+ 小于： **\$lt**  
>MongoDB ： db.collection.find({ price:{ **\$lt:** 100 }})
>RDBMS ： where likes <= 100 
+ 大于等于： **\$gte**  
>MongoDB ： db.collection.find({ price:{ **\$gte:** 100 }})
>RDBMS ： where likes > 100 
+ 小于等于： **\$lte**  
>MongoDB ： db.collection.find({ price:{ **\$lte:** 100 }})
>RDBMS ： where likes >= 100
+ 区间：
>查找 price 属于区间 (100,200] 的文档数据:
>db.collection.find({ price:{ **\$gt:** 100,**\$lte:** 200 }})` 


## 13.MongoDB $type 操作符
----------------------------------------------------------------------

+ 基于BSON类型，检索集合中匹配 **指定数据类型** 的数据 ，并返回结果。
>如果想获取 "collection" 集合中 title 为 String 的数据，你可以使用以下命令：
`db.collection.find({"title" : {$type : 2}})`
或
`db.collection.find({"title" : {$type : 'string'}})`
+ MongoDB 中可以使用的类型如下表所示：

类型 | 数字 | 备注
:---|:---|:---
Double | 1 |  
String | 2 |  
Object | 3 |  
Array | 4 |  
Binary data | 5 |  
Undefined | 6 | 已废弃。
Object id | 7 |  
Boolean | 8 |  
Date | 9 |  
Null | 10 |  
Regular Expression | 11 |  
JavaScript | 13 |  
Symbol | 14 |  
JavaScript (with scope) | 15 |  
32-bit integer | 16 |  
Timestamp | 17 |  
64-bit integer | 18 |  
Min key | 255 | Query with -1.
Max key | 127	 


## 14.MongoDB limit与skip方法
----------------------------------------------------------------------

+ **limit()：** 接受一个数字参数， 该参数指定从MongoDB中读取的记录条数。
`db.COLLECTION_NAME.find().limit(NUMBER)`
+ **skip()：** 接受一个数字参数， 该参数指定读取数据前需要跳过的记录条数。
`db.COLLECTION_NAME.find().skip(NUMBER)`
+ **limit() 与 skip() 组合：**
`db.COLLECTION_NAME.find().limit(NUMBER).skip(NUMBER)`


## 15.MongoDB 排序
----------------------------------------------------------------------
+ **sort()：** 可以通过参数指定排序的字段，并使用 1 和 -1 来指定升序和降序。
`db.COLLECTION_NAME.find().sort({key_name:1})`


## 16.MongoDB 索引
----------------------------------------------------------------------
+ 创建索引
`db.collection.createIndex(keys, options)`
`db.collection.ensureIndex(keys, options) // 旧版本`
+ 注：均使用 1 和 -1 来指定升序和降序
+ 注：如果现有的索引字段的值超过索引键的限制，MongoDB中不会创建索引。
+ 注：如果文档的索引字段值超过了索引键的限制，MongoDB不会将任何文档转换成索引的集合。
+ 注：存储在内存(RAM)中,你应该确保该索引的大小不超过内存的限制。否则，MongoDB会删除一些索引。

最大范围：
- 集合中索引不能超过64个
- 索引名的长度不能超过128个字符
- 一个复合索引最多可以有31个字段

创建索引可选参数列表如下:
参数 | 类型 | 描述
:---|:---|:---
background | Boolean | 建索引过程会阻塞其它数据库操作，background可指定以后台方式创建索引，即增加 "background" 可选参数。 "background" 默认值为false。
unique | Boolean | 建立的索引是否唯一。指定为true创建唯一索引。默认值为false.
name | string | 索引的名称。如果未指定，MongoDB的通过连接索引的字段名和排序顺序生成一个索引名称。
dropDups | Boolean | 3.0+版本已废弃。在建立唯一索引时是否删除重复记录,指定 true 创建唯一索引。默认值为 false.
sparse | Boolean | 对文档中不存在的字段数据不启用索引；这个参数需要特别注意，如果设置为true的话，在索引字段中不会查询出不包含对应字段的文档.。默认值为 false.
expireAfterSeconds | integer | 指定一个以秒为单位的数值，完成 TTL设定，设定集合的生存时间。
v | index version | 索引的版本号。默认的索引版本取决于mongod创建索引时运行的版本。
weights | document | 索引权重值，数值在 1 到 99,999 之间，表示该索引相对于其他索引字段的得分权重。
default_language | string | 对于文本索引，该参数决定了停用词及词干和词器的规则的列表。 默认为英语
language_override | string | 对于文本索引，该参数指定了包含在文档中的字段名，语言覆盖默认的language，默认值为 language.

+ 创建单Key索引 
> db.collection.createIndex( {age: 1} )
+ 创建复合索引 (按照指定Key的先后顺序进行索引，不能直接跳过前面的Key进行索引)
> db.collection.createIndex( {age: 1, name: 1} )
+ 创建多Key索引 （索引的Key为**数组**，会此数组的每个元素建立一条索引）
> {age = 1,knowledge = ["C++","Python"],}      // 需要索引的集合举例
> db.collection.createIndex( {knowledge: 1} )  // 多Key索引
+ 文档中有子集合字段： 通过{"key.子Key":1} 建立索引
> {"address": {"city": "Los Angeles","state": "California","pincode": "123"},}
> db.collection.createIndex( {"address.city": 1} )  // 子集合索引

+ 全文检索
> // 开启全文检索 ， （MongoDB 2.6之后默认开启）
> db.adminCommand({setParameter:true,textSearchEnabled:true})
> // 或者使用命令开启
> mongod --setParameter textSearchEnabled=true
> // 创建全文索引
> db.collection.createIndex({post_text:"text"})
> // 使用全文索引
> db.collection.find({\$text:{\$search:"runoob"}})

+ 查看集合索引
> db.collection.getIndexes()
+ 查看集合索引大小
> db.collection.totalIndexSize()
+ 删除集合所有索引
> db.collection.dropIndexes()
+ 删除集合指定索引
> db.collection.dropIndex("索引名称")

索引不能被以下的查询使用：
+ 正则表达式及非操作符，如 \$nin, \$not, 等。
+ 算术运算符，如 \$mod, 等。
+ \$where 子句
+ **所以**，检测你的语句是否使用索引是一个好的习惯，可以用explain()来查看。

+ **TTL索引** (*) :
  - 文档过期自动删除的应用在单Key索引。
  `db.collection.createIndex( { "index_key": 1 }, { expireAfterSeconds: 3600 } )`
  - 如果 索引字段 或者 expireAfterSeconds参数 是数组，并且索引中有多个日期值，则MongoDB会使用其中最早的日期值来计算到期值。
  - 到期值 = "index_key"的值 + expireAfterSeconds参数的Date值 或者 expireAfterSeconds数组的 **最小** Date值。
  - 如果索引字段不是Date类型或者包含Date类型的数组，则文档将不会过期。
  - 如果文档不包含索引字段，则文档将不会过期。
  - 不支持 capped collection 固定集合。
  - 不支持"_id"。
  - 过期后 ， 默认会在 **60秒** 内删除该文档。（MongoDB后台任务每60秒运行一次）
  - expireAfterSeconds设置后 ， 不能改变。


## 17.MongoDB 聚合 (*)
----------------------------------------------------------------------
+ 通过各种函数，定义管道的一系列操作，对文档的数据进行灵活的查询、分类、提取等操作。
  >原始数据 ----> 管道操作1 ----> 管道操作2 ----> 管道操作3 ----> ... ----> 输出数据
+ aggregate() : 
  >db.COLLECTION_NAME.aggregate([{管道操作1},{管道操作2},{管道操作3},...],options) ， 返回一个指向结果的指针（*）。
  
+ **options**: `{ explain:true, allowDiskUse:true, cursor:{batchSize:n} }`
  **explain**：运行管道 ， 并且返回管道处理的详细信息。
    > 用于检测管道的可行性。

  **allowDiskUse**：  使用磁盘储存数据。
    > 用于查询的数据过大超过了Ram内存的限制。
    > 因为会使用到磁盘， 所以性能会降低，因此建议在需要的时候才使用。
    > 在使用前，必须先使用 \$match 和 \$project 进行初始数据的筛选。

  **cursor**：指定初始批处理的大小。 通过返回少量文档结果处理大的结果集。
    > 结果返回的cursor可以进行如下操作：
    > cursor.hasNext()  **----------->** 结果集中是否存在下一个元素
    > cursor.next()     **----------->** 返回结果集的下一个元素
    > cursor.forEach()  **----------->** 遍历结果集的每一行
    > cursor.map()      **----------->** 遍历结果集的每一行，返回一个结果**数组**
    > cursor.toArray()  **----------->** 以数组的形式返回结果，(所有结果会 **立即** 读入内存)
    > cursor.pretty()   **----------->** 显示格式化后的结果，(所有结果会 **立即** 读入内存)
    > cursor.itcount()  **----------->** 返回结果数量（仅有数量，不包含结果，建议直接使用 **\$group** 管道处理）

+ **聚合管道:** MongoDB文档在一个管道处理完毕后，将结果传递给下一个管道处理，管道操作是可以重复的。 
  - **\$project :** 修改输入文档的结构。可以用来重命名、增加或删除域，也可以用于创建计算结果以及嵌套文档，类似**投影**。
  - **\$group :** 将集合中的所有文档根据字段进行**分组**、**统计**。（具体见下方）
  - **\$match :** 用于过滤数据，只输出符合条件的文档。$match使用MongoDB的**标准查询操作**。
  - **\$limit :** 用来**限制**MongoDB聚合管道**返回**的文档数。
  - **\$skip :** 在聚合管道中**跳过**指定数量的文档，并返回余下的文档。
  - **\$sort :** 将输入文档**排序**后输出。
  - **\$unwind :** 将文档中的某一个数组类型字段**拆分**成多条，每条包含**数组**中的一个值。
  - **\$out :** 把管道的结果**输出到**一个指定名字的**集合**里，此管道必须是**最后一个操作**管道。
  - **\$geoNear :** 输出接近某一地理位置的有序文档。
  - **\$redact :** 控制特定数据的访问。

    > **例子**：
    > // 获取一个只剩下_id,tilte和author三个字段的集合： ($project示例)
    > db.article.aggregate( { \$project : { title : 1 ,author : 1} } );
    > // 获取分数大于70小于或等于90记录，然后将符合条件的记录送到下一阶段\$group管道操作符进行处理：(\$match示例)
    > db.articles.aggregate( [{ \$match : { score : { \$gt : 70, \$lte : 90 } } }, { \$group: { _id: null, count: { \$sum: 1 } } } ] );
    > // "过滤"掉前五个文档: (\$skip示例)
    > db.article.aggregate( { \$skip : 5 } );

+ **\$group** 相关函数：
    表达式 | 描述 | 实例
    :---|:---|:---
    \$sum | 计算集合中所有文档的指定字段的**总和**。 | db.collection.aggregate([{**\$group: {** _id : "\$by_user", num_tutorial : {**\$sum** : "\$likes"} **}** }])
    \$avg | 计算集合中所有文档的指定字段的**平均值** | db.collection.aggregate([{**\$group: {** _id : "\$by_user", num_tutorial : {**\$avg** : "\$likes"} **}** }])
    \$min | 获取集合中所有文档的指定字段的**最小值**。 | db.collection.aggregate([{**\$group: {** _id : "\$by_user", num_tutorial : {**\$min** : "\$likes"} **}** }])
    \$max | 获取集合中所有文档的指定字段的**最大值**。 | db.collection.aggregate([{**\$group: {** _id : "\$by_user", num_tutorial : {**\$max** : "\$likes"} **}** }])
    \$first | 根据源文档的**排序结果**获取**第一个**文档数据。 | db.collection.aggregate([{**\$group: {** _id : "\$by_user", first_url : {**\$first** : "\$url"} **}** }])
    \$last | 根据源文档的**排序结果**获取**最后一个**文档数据 | db.collection.aggregate([{**\$group: {** _id : "\$by_user", last_url : {**\$last** : "\$url"} **}** }])
    \$push | 在**结果文档**中插入值到一个数组中。 | db.collection.aggregate([{**\$group: {** _id : "\$by_user", url : {**\$push**: "\$url"} **}** }])
    \$addToSet | 在**结果文档**中插入值到一个数组中，**不允许重复**。 | db.collection.aggregate([{**\$group: {** _id : "\$by_user", url : {**\$addToSet** : "\$url"} **}** }])

+ **重塑文档** ：
  - 使用聚合管道把源文档通过各类函数生成一个与源文档不一样的新文档。
  - 常常与 \$project 和 \$group 使用。
  - MongoDB官网文档： https://docs.mongodb.com/manual/reference/operator/aggregation/group/

  - 字符串函数
    表达式 | 描述
    :---|:--
    \$concat | 连接2个或者更多字符串为一个字符串
    \$strcasecmp | 大小写敏感的比较，返回数字
    \$substr | 获取字符串的子串, {\$substr:["string", start_index, end_index]}
    \$toLower | 转换为小写字母
    \$toUpper | 转换为大写字母

  - 算术函数
    表达式 | 描述
    :---|:--
    \$add | 求和
    \$divede | 除法
    \$mod | 求余数
    \$multiply | 乘积
    \$subtract | 减法

  - 日期函数
    表达式 | 描述
    :---|:--
    \$dayOfYear | 一年365天中的某一天
    \$dayOfMouth | 一月中的某一天
    \$dayOfWeek | 一周中的某一天， 1表示周日
    \$year | 日期的年份
    \$mouth | 日期的月份，1~12
    \$week | 一年中的某一周，0~53
    \$hour | 日期的小时，0~23
    \$minute | 日期的分钟，0~59
    \$second | 日期的秒，0~59
    \$millisecond | 日期的毫秒，0~999

  - 逻辑函数
    表达式 | 描述
    :---|:--
    \$and true | 与操作，如果数组里所有值都为true，则返回true
    \$or | 或，如果数组中有一个true ， 就返回true
    \$cmp | 如果2个数相等就返回 0
    \$cond if... then... else | 条件逻辑 （类似三元操作）
    \$eq | 2个值是否相等
    \$gt | 值1是否大于值2
    \$gte | 值1是否大于等于值2
    \$lt | 值1是否小于值2
    \$lte | 值1是否小于等于值2
    \$ne | 值1是否不等于值2
    \$not. | 取反操作
    \$ifNull | 把 null 值/表达式转换为特定的值

  - 集合操作符
    表达式 | 描述
    :---|:--
    \$setEquals | 如果两个集合的元素完全相同，则为true
    \$setIntersection | 返回两个集合的公共元素
    \$setDifference | 返回第一个集合中与第二个集合不同的元素
    \$setUnion | 合并集合
    \$setIsSubset | 如果第二个集合为第一个集合的子集，则为true
    \$anyElementTrue | 如果某个集合元素为true ， 则为true
    \$allElementTrue true | 如果所有集合元素都为true ， 则为true

  - 其他
    表达式 | 描述
    :---|:--
    \$meta | 文本搜索
    \$size | 返回数组大小
    \$map | 对数组的每个成员应用表达式
    \$let | 定义表达式内使用的变量
    \$literal | 返回表达式的值，而不评估它

+ **.count(条件)** 可以查询统计符合条件的集合的总数，但在分布式集合中，会出现计算错误的情况。
+ **.distinct()** 可以找出给定键的所有去重之后的值。使用时也必须指定集合和键
  `db.collection.distinct(查询的集合, 去重的字段, 选项)`
+ **Map-Reduce**：
  - Map-Reduce是一种计算模型，简单的说就是将大批量的数据分解执行（MAP），然后再将结果合并成最终结果（REDUCE）。
  - Map-Reduce是聚合功能的首次尝试，比聚合框架要慢。
  - Map函数和Reduce函数可以使用**JavaScript** 实现：
  ```
  db.collection.mapReduce(
    function() {emit(key,value);},  //map 函数 , 必须返回 emit()函数 ， 把原集合按Key分组，得到{key - values数组}集合。
    function(key,values) {return reduceFunction},   //reduce 函数, 把 values数组 变成一个 value值 ，把{key - values数组}集合变成{key - value值}集合
    {
        out: collection,    //统计结果存放集合 (不指定则使用临时集合,在客户端断开后自动删除)。
        query: document,    //一个筛选条件，只有满足条件的文档才会调用map函数。（query。limit，sort可以随意组合）
        sort: document,     //和limit结合的sort排序参数（也是在发往map函数前给文档排序），可以优化分组机制
        limit: number       //发往map函数的文档数量的上限（要是没有limit，单独使用sort的用处不大）
    }
  )
  ```
  - mapReduce函数的打印结果解析：
  > **result：** 储存结果的collection的名字,这是个临时集合，MapReduce的连接关闭后自动就被删除了。
  > **timeMillis：** 执行花费的时间，毫秒为单位
  > **input：** 满足条件被发送到map函数的文档个数
  > **emit：** 在map函数中emit被调用的次数，也就是所有集合中的数据总量
  > **ouput：** 结果集合中的文档个数（count对调试非常有帮助）
  > **ok：** 是否成功，成功为1
  > **err：** 如果失败，这里可以有失败原因，不过从经验上来看，原因比较模糊，作用不大


## 18.MongoDB 复制（副本集 replica set） 
----------------------------------------------------------------------
+ 将数据同步在多个服务器的过程。
+ 提供了数据的冗余备份，并在多个服务器上存储数据副本，提高了数据的可用性， 并可以保证数据的安全性。
+ 还允许您从硬件故障和服务中断中恢复数据。
  > 复制：
  > 1.保障数据的安全性
  > 2.数据高可用性 (24*7)
  > 3.灾难恢复
  > 4.无需停机维护（如备份，重建索引，压缩）
  > 5.分布式读取数据

  > 副本集：
  > 1.N个节点的集群
  > 2.任何节点可作为主节点
  > 3.所有写入操作都在主节点上
  > 4.自动故障转移
  > 5.自动恢复

+ **原理：** 主节点记录在其上的所有操作**oplog**，从节点定期轮询主节点获取这些操作，然后对自己的数据副本执行这些操作，从而保证从节点的数据与主节点一致。 
+ 相关网站：
https://www.jb51.net/article/109091.htm
https://www.cnblogs.com/6luv-ml/p/9187435.html
https://blog.csdn.net/tao1992/article/details/70211966

MongoDB副本集设置步骤:
1. 关闭现有的MongoDB数据库,备份（并清空原来的）数据。
2. 通过指定 --replSet 来启动MongoDB:
`mongod --port "PORT" --dbpath "YOUR_DB_DATA_PATH" --replSet "REPLICA_SET_INSTANCE_NAME"`
3. 在Mongo客户端使用 rs.initiate() 启动一个新的副本集
4. 在Mongo客户端使用 rs.conf() 查看副本集的配置
5. 在Mongo客户端使用 rs.status() 查看副本集状态
6. 在Mongo客户端使用 rs.add() 添加副本集成员
`rs.add(HOST_NAME:PORT)`
7. 只能通过 **主节点** 将Mongo服务添加到副本集
8. 使用 db.isMaster() 判断当前运行的Mongo服务是否为主节点


## 19.MongoDB 分片（*）
----------------------------------------------------------------------

## 20.MongoDB 备份和恢复（*）
----------------------------------------------------------------------
+ 备份
> mongodump
+ 恢复
> mongorestore
+ 默认备份目录
> MongoDB 会在当前 dbPath 目录下创建一个 dump 目录，并把所有的数据库按**数据库名称**创建目录。 
+ 备份参数
> // 此命令将备份指定的 mongod 实例的所有数据库。
> mongodump —host HOST_NAME —port PORT_NUMBER
> // 此命令将仅备份指定数据库的指定集合。
> mongodump —collection COLLECTION —db DB_NAME
> // 此命令将仅在指定路径上备份数据库。
> mongodump —out BACKUP_DIRECTORY


## 21.MongoDB 监控（*）
----------------------------------------------------------------------

## 22.文档关系
----------------------------------------------------------------------
+ 嵌入式： 把文档直接插入另一个文档以建立关系。
+ 引用式： 通过引用文档的 id 字段来建立关系。

<br>
## 23.MongoDB 数据库引用
----------------------------------------------------------------------
+ DBRefs：一个文档从多个集合引用文档
```
"Key" = {
  $ref："引用的集合名称",//直接用db[Key.$ref]获得集合
  $id：引用的文档id,
  $db："引用的数据库名称，可选参数",
}
```

## 24.MongoDB 覆盖索引查询（*）
----------------------------------------------------------------------
+ 所有的查询字段是索引的一部分
+ 所有的查询返回字段在同一个索引中
+ 所有索引字段是一个数组，则不能使用覆盖索引查询。

## 25.MongoDB 查询分析（*）
----------------------------------------------------------------------
+ explain() : 提供了大量与查询相关的信息，使用索引及查询统计等。有利于我们对索引的优化，是最重要的诊断工具之一。
+ hint() : 强制 MongoDB 使用一个指定的索引，必须要确保此索引已被建立。
`db.users.find({"username":"user1000", "age":30}).hint({"username":1}) // 强制使用索引{"username":1} `

## 26.MongoDB GridFS
----------------------------------------------------------------------
+ GridFS 用于存储和恢复那些超过16M（BSON文件限制）的文件(如：图片、音频、视频等)。
+ GridFS 把文件存储在MonoDB的集合中，用两个集合来存储一个文件：
  fs.files  保存和文件有关的meta数据(filename,content_type,还有用户自定义的属性)
  fs.chunks 保存每个文件的实际内容(二进制数据)，一般每个chunk为256k
```
// 使用命令添加文件
mongofiles.exe -d gridfs put song.mp3
// 查看数据库中的文件的信息
db.fs.files.find()
// 根据 _id 获取 chunk 的数据
db.fs.chunks.find({files_id:ObjectId('xxxxxxx')})
```

## 27.MongoDB 正则表达式
----------------------------------------------------------------------
+ MongoDB 使用 $regex 操作符来设置匹配字符串的正则表达式。
+ MongoDB使用PCRE (Perl Compatible Regular Expression) 作为正则表达式语言。
+ 不同于全文检索，我们使用正则表达式不需要做任何配置。
- 以下命令使用正则表达式查找包含 runoob 字符串的文章：
`db.posts.find({post_text:{$regex:"runoob"}})`
- 以上查询也可以写为：
`db.posts.find({post_text:/runoob/})`
- 以下命令将查找不区分大小写的字符串 runoob：(设置 **\$options:"\$i"**)
`db.posts.find({post_text:{$regex:"runoob",$options:"$i"}})`
- 在数组字段中使用正则表达式来查找内容
`db.posts.find({数组名字:{$regex:"run"}})`
