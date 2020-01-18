# 哈利波特阅读网站

哈利波特阅读网站项目，包括网页前端(frontend)，网站后端(backend)以及手机App前端(尚未开始)。

## 功能设计

### 网页
在线阅读英文版书籍，目前主要是哈利波特。

- 文字排版，标题 作者 章节 段落
- 悬浮显示单词翻译
- 记录某个单词
- 记录某个句子
- 复制单词句子

### APP
使用app阅读记录的单词与句子

- 查看记录的单词
  - 形式: 普通列表，每一项包括{单词 发音 释义}, 列表项显示全部内容
- 查看记录的句子
  - 形式: 卡片式列表，卡片中为句子内容
- 一次获得全部单词


## API设计

包括翻译，词、句记录，App前端数据等API

| name            | request                      | response                                                                                                            |
| --------------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| wordtrans       | GET wordtrans?word=xxx       | {"word": "about","phonetic": "ә'baut","translation": "prep. 在...周围，大约 有关 关于\nadv. 大约 四处 在附近 周围"} |
| wordrec         | GET wordrec?word=xxx         | {"staus":1}                                                                                                         |
| sentencerec     | GET sentencerec?sentence=xxx | {"staus":1}                                                                                                         |
| app-allword     | GET appallword               | {}                                                                                                                  |
| app-allsentence | GET appallsentence           | {}                                                                                                                  |
