'''
uwsgi服务器脚本文件
'''

import json
import sys
from urllib import parse
import mysql.connector as connector


host = '127.0.0.1'
user = 'sjf'
passwd = '123456'
port = 3306

dbName = 'reader_hp'
dictTableName = 'wordDict'
wordRecTableName = "wordRecord"
sentenceRecTableName = "sentenceRecord"

debug = False

conn = None

# ------------------------------------------


def log(s1):
    if debug:
        print("--------------------------\n%s\n--------------------------" % (s1), file=sys.stderr)


def replaceQuote(s: str):
    """ 将 s 中的 " 替换为 \\" """
    return s.replace('"', '\\"')


def makeTrans(tup: tuple):
    """ 生成一个字典格式的单词释义"""
    def toStr(s):
        return s if type(s) is str else str(s, encoding="utf-8")
    res = None
    if len(tup) >= 4:
        res = {
            "word": toStr(tup[0]),
            "phonetic": toStr(tup[1]),
            "translation": toStr(tup[2]),
            "exchange": toStr(tup[3])
        }
    # log("makeTrans, res: %s" % (res))
    return res

# ------------------------------------------


def getDBConnection():
    global conn
    """ 连接到数据库，返回连接对象 """
    conn = connector.connect(user=user, passwd=passwd, database=dbName)
    return conn


def queryWord(word: str, conn: connector.MySQLConnection, tableName=dictTableName):
    """ 从数据库查询单词，返回 tuple 或 none """
    # for s in word:
    #     if not s.isalpha() and not s == '-':
    #         return None
    cursor = conn.cursor()
    cursor.execute("select * from %s where word = \"%s\";" % (tableName, word))
    return cursor.fetchone()


def insertWordRecToDB(wordRec, conn: connector.MySQLConnection):
    """ 将一个 wordRec 插入到数据库中，若单词已存在则不插入， wordRec 为 dict 格式的对象，
    返回 True / False 表示是否插入 """
    if queryWord(wordRec["word"], conn, tableName=wordRecTableName) is None:
        for key in wordRec.keys():
            replaceQuote(wordRec[key])
        cursor = conn.cursor()
        cursor.execute('insert into %s values("%s", "%s", "%s", "%s")' % (
            wordRecTableName,
            wordRec["word"], wordRec["phonetic"], wordRec["translation"], wordRec["exchange"]
        ))
        cursor.close()
        conn.commit()
    return True


def insertSenRecToDB(sentence, conn: connector.MySQLConnection):
    """ 将句子插入到数据库中，返回 True """
    cursor = conn.cursor()
    sentence = replaceQuote(sentence)
    cursor.execute('select * from %s where sentence = "%s"' % (
        sentenceRecTableName, sentence))
    if (cursor.fetchone() is None):
        cursor.execute('insert into %s (sentence) values ("%s")' % (
            sentenceRecTableName, sentence))
        conn.commit()
    cursor.close()
    return True


# -------------------------------------------


def wordTrans(word):
    """ 翻译单词，从数据库读取数据，返回 字典对象 / none """
    transTuple = queryWord(word, getDBConnection())
    # log("wordTrans, word: %s, tuple: %s" % (word, str(transTuple)))
    return makeTrans(transTuple) if transTuple is not None else None


def wordRec(word):
    """ 记录单词，如果找不到单词释义，返回 False，如果单词已经记录，返回 True，
    否则将单词加入数据库，返回 True """
    tmpTransTuple = queryWord(word, getDBConnection())
    if tmpTransTuple is not None:
        return insertWordRecToDB(makeTrans(tmpTransTuple), getDBConnection())
    return False


def sentenceRec(sentence):
    """ 记录句子，返回 True """
    return insertSenRecToDB(sentence, getDBConnection())


def allWords():
    """ 获取所有单词，返回列表 """
    cursor = getDBConnection().cursor()
    cursor.execute("select * from %s" % (wordRecTableName))
    resList = cursor.fetchall()
    conn.close()
    retList = []
    for res in resList:
        retList.append(makeTrans(res))
    return retList


def allSentences():
    """ 获取所有句子，返回列表 """
    cursor = getDBConnection().cursor()
    cursor.execute("select * from %s" % (sentenceRecTableName))
    resList = cursor.fetchall()
    conn.close()
    # log(resList.__str__())
    retList = [{"sentence": (x[1] if type(x[1]) is str else str(x[1], encoding="utf-8"))} for x in resList]
    return retList


def dispatch(path, paraDict):
    """
    根据 path 执行相应的函数，返回一个对象{"status": 0/1, "data": {}}
    """
    res = {"status": 0}
    prefix = "/cgi/"

    if path[0: len(prefix)] != prefix:
        return res
    path = path[len(prefix):]

    if path == "wordtrans" and "word" in paraDict:
        res["data"] = wordTrans(paraDict["word"][0])
        res["status"] = (1 if res["data"] is not None else 0)

    elif path == "wordrec" and "word" in paraDict:
        res["data"] = wordRec(paraDict["word"][0])
        res["status"] = (1 if res["data"] is True else 0)

    elif path == "sentencerec" and "sentence" in paraDict:
        res["data"] = sentenceRec(paraDict["sentence"][0])
        res["status"] = (1 if res["data"] is True else 0)

    elif path == "allwords":
        res["data"] = allWords()
        res["status"] = (1 if res["data"] is not None else 0)

    elif path == "allsentences":
        res["data"] = allSentences()
        res["status"] = (1 if res["data"] is not None else 0)

    else:
        pass
    return res


def application(env, start_response):
    if env["PATH_INFO"] == "/":
        start_response("200 OK", [("Content-Type", "text/html")])
        return [b'<html><script>location.href = "/static/index.html";</script></html>']
    res = dispatch(env["PATH_INFO"], parse.parse_qs(env["QUERY_STRING"]))
    start_response("200 OK", [('Content-Type', 'text/plain;charset=UTF-8')])
    return [json.dumps(res, ensure_ascii=False, indent=4).encode()]
