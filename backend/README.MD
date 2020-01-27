# 英文阅读网站App后端

为网站提供json格式的书籍信息、查询单词释义、记录词句的信息，为App提供查询所有已记录词句的功能。后端目前采用[halox](https://github.com/EricJeffrey/my_http_server)+python程序实现，halox需要从源码构建。

## 部分文件说明

如下为构建后端时用到的文件说明

- make*db.py: 构造字典数据库的Python文件
- testdb.py: 测试字典数据库的Python文件
- svr/halox.conf: halox服务器的配置文件，包括监听端口、地址、url对应的文件

## 功能实现

- 获取单词翻译
  > 前端发送单词，从数据库查询对应单词释义，若查询到，返回`{status: 1, data: {translation}}`，否则发挥`{status: 0, data: {}}`
- 记录单词
  > 前端发送单词，从数据库获取单词释义，若查询到，将单词及释义添加到`wordRecord`表中
- 记录句子
  > 前端发送句子，将句子加入到`sentenceRecord`中
- 获取所有单词
  > 从`wordRecord`中获取所有单词发送到前端
- 获取所有句子
  > 从`sentenceRecord`获取中获取所有句子发送到前端