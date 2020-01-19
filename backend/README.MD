# 英文阅读网站App后端

为网站提供json格式的书籍信息、查询单词释义、记录词句的信息，为App提供查询所有已记录词句的功能。后端目前采用[halox](https://github.com/EricJeffrey/my_http_server)+python程序实现，halox需要从源码构建。

## 部分文件说明

如下为构建后端时用到的文件说明

- makedb.py: 构造字典数据库的Python文件
- testdb.py: 测试字典数据库的Python文件
- svr/halox.conf: halox服务器的配置文件，包括监听端口、地址、url对应的文件