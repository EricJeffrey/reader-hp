'''
处理单词记录请求，获取单词翻译并记录到数据库中
'''

import json
import os
import mysql.connector as connector

dbName = "reader_hp"
dictTableName = 'wordDict'
wordRecTableName = 'wordRecord'


def parseQuery(queryStr: str):
    '''
    解析url中的请求参数，queryStr为字符串形式的请求参数，格式如下

    a=xxx&b=xxx&sd

    返回一个包含所有请求参数的dict对象
    '''
    res = {}
    for singleQuery in queryStr.split('&'):
        if '=' in singleQuery:
            tmpList = singleQuery.split('=')
            res[tmpList[0]] = tmpList[1]
        else:
            res[singleQuery] = ""
    return res


def queryWord(word: str, conn: connector.MySQLConnection):
    '''
    从数据库中查询 word 对应的记录

    返回 tuple=obj/none
    '''
    for s in word:
        if not s.isalpha() and not s == '-':
            return None
    cursor = conn.cursor()
    cursor.execute("select * from %s where word = '%s'" % (dictTableName, word))
    ret = cursor.fetchone()
    cursor.close()
    return ret


def addToWordRec(data, conn: connector.MySQLConnection):
    '''
    记录单词，data格式为{"word":x, "phonetic":x, "translation":x, "exchange":x}

    返回 true 表示将单词加入了数据库或已存在，false表示未加入或出现了问题
    '''
    # 判断是否已经包含单词
    cursor = conn.cursor()
    cursor.execute("select * from %s where word = '%s'" % (wordRecTableName, data["word"]))
    for key in data.keys():
        data[key] = data[key].replace('"', '\\"')
    if (cursor.fetchone() is None):
        cursor.execute('insert into %s values("%s", "%s", "%s", "%s")' % (
            wordRecTableName, data["word"], data["phonetic"], data["translation"], data["exchange"]
        ))
    cursor.close()
    return True


def work():
    reqPara = parseQuery(os.environ["query"])
    resp = {"status": 0}
    if 'word' in reqPara:
        conn = connector.connect(user="root", passwd="123456", database=dbName)
        tmpTrans = queryWord(reqPara['word'], conn)
        if tmpTrans != None:
            resp["status"] = 1
            data = {
                "word": tmpTrans[0],
                "phonetic": tmpTrans[1],
                "translation": tmpTrans[2],
                "exchange": tmpTrans[3]
            }
            addToWordRec(data, conn)
            conn.commit()
    print(json.dumps(resp, ensure_ascii=False))


if __name__ == "__main__":
    work()
