'''
记录句子 - 将句子加入到数据库中
'''

from urllib import parse
import json
import os
import mysql.connector as connector

dbName = "reader_hp"
sentenceRecTableName = "sentenceRecord"


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


def addToSentenceRec(sentence, conn: connector.MySQLConnection):
    cursor = conn.cursor()
    sentence = sentence.replace('"', '\\"')
    cursor.execute('select * from %s where sentence = "%s"' % (sentenceRecTableName, sentence))
    if (cursor.fetchone() is None):
        cursor.execute('insert into %s (sentence) values ("%s")' % (sentenceRecTableName, sentence))
        conn.commit()
    cursor.close()
    return True


def work():
    reqPara = parseQuery(os.environ["query"])
    resp = {"status": 0}
    if "sentence" in reqPara:
        sentence = parse.unquote(reqPara["sentence"])
        conn = connector.connect(user="root", passwd="123456", database=dbName)
        addToSentenceRec(sentence, conn)
        resp["status"] = 1
    print(json.dumps(resp, ensure_ascii=False))

if __name__ == "__main__":
    work()
