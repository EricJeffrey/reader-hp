'''
处理单词翻译请求，os.environ 中的 query 字段包含了请求参数
解析请求参数后从数据库读取内容
返回如下格式的json
{"status": 1/0, "data":{"word": "xxx","phonetic": "xxx","translation": "xxxStr\nxxx"}}
status 为0表示没有查询到翻译
'''

import json
import os
import mysql.connector as connector

dbName = "reader_hp"
dictTableName = 'wordDict'


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
    cursor.execute("select * from %s where word = '%s'" %
                   (dictTableName, word))
    return cursor.fetchone()


#  todo halox 文件类型 响应截断最后字符 cgi管理器
if __name__ == "__main__":
    reqPara = parseQuery(os.environ["query"])
    resp = {"status": 0, "data": {}}
    if 'word' in reqPara:
        conn = connector.connect(user="root", passwd="123456", database=dbName)
        tmpTrans = queryWord(reqPara['word'], conn)
        if tmpTrans != None:
            resp["status"] = 1
            resp["data"] = {
                "word": tmpTrans[0],
                "phonetic": tmpTrans[1],
                "translation": tmpTrans[2],
                "exchange": tmpTrans[3]
            }
    print(json.dumps(resp, ensure_ascii=False))
