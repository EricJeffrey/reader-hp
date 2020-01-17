# 哈利波特阅读网站

哈利波特阅读网站项目，包括网页前端(frontend)，网站后端(backend)以及手机App前端(尚未开始)。

## API设计

包括翻译，词、句记录，App前端数据等API

- 单词翻译
  - 请求: `GET addr?q=word`
  - 响应: JSON
    ```json
    {
        "word": "about",
        "phonetic": "ә'baut",
        "translation": "prep. 在...周围，大约 有关 关于\nadv. 大约 四处 在附近 周围"
    }
    ```
- 单词记录
- 句子记录
- App