'''
字典数据库处理
从edict.csv(https://github.com/EricJeffrey/ECDICT)获取英文字典数据，连接到mysql数据库[reader_hp]并创建表[wordDict]
将所有单词，包括单词的过去式、过去分词、现在分词、第三人称单数、比较级、最高级、名词复数形式插入到数据库中。

单词的形式作为新记录，若某个形式已作为其它词类存在，则在其后增加一条说明(e.g. xxx的比较级)
'''

import random
import sys
import mysql.connector as connector
import csv
import json
import resource

'''
res line num: 693205
max translation len: 372
'''

# 数据库名
dbName = "reader_hp"
dictTableName = 'wordDict'
dictTableCols = [
    ['word', 'varchar(255) BINARY'],
    ['phonetic', 'varchar(255)'],
    ['translation', 'varchar(1000)'],
    ['exchange', 'varchar(255)'],
]


def checkAtoZSpace(s: str):
    '''
    检查字符串是否只包含字母和空格
    '''
    # for ch in s:
    #     if (not ch.isalpha()) and (not ch.isspace()):
    #         return False
    return True


def process():
    '''
    将所有内容记录到内存并返回
    '''
    with open("ecdict.csv", "r", encoding="utf-8") as csvfp:
        reader = csv.reader(csvfp)
        reader.__next__()
        # 限制数量
        n = 770612
        resList = []
        wordset = set()
        for i in range(1, n):
            if i % 10000 == 0:
                print(i / 10000)
            row = reader.__next__()
            # 只保留短语和单词
            if row[0] in wordset or not checkAtoZSpace(row[0]):
                continue
            resList.append(
                {"word": row[0], "phonetic": row[1], "translation": row[3], "exchange": row[10]})
            wordset.add(row[0])
        # 保存单词的各种形式
        expandResList = []
        for tmpres in resList:
            if len(tmpres["exchange"]) > 1:
                # 所有形式
                tmpWordExcList = tmpres["exchange"].split('/')
                for wordExcStr in tmpWordExcList:
                    # 每个形式
                    tmpType = wordExcStr[0:1]
                    tmpWordExc = wordExcStr[2:]
                    # 已经有这个形式，不考虑 词元
                    if (tmpWordExc in wordset) or (tmpType == "0" or tmpType == '1'):
                        continue
                    wordset.add(tmpWordExc)
                    tmpExpandRes = {
                        "word": tmpWordExc, "phonetic": tmpres["phonetic"], "translation": tmpres["translation"] + "\n", "exchange": ""}
                    tmpStr = ""
                    if tmpType == 'p':
                        tmpStr += tmpres["word"] + "的过去式"
                    elif tmpType == 'd':
                        tmpStr += tmpres["word"] + "的过去分词"
                    elif tmpType == 'i':
                        tmpStr += tmpres["word"] + "的现在分词"
                    elif tmpType == '3':
                        tmpStr += tmpres["word"] + "的第三人称单数形式"
                    elif tmpType == 'r':
                        tmpStr += tmpres["word"] + "的比较级"
                    elif tmpType == 't':
                        tmpStr += tmpres["word"] + "的最高级"
                    elif tmpType == 's':
                        tmpStr += tmpres["word"] + "的名词复数"
                    tmpExpandRes["translation"] = tmpStr + \
                        "\n" + tmpExpandRes["translation"]
                    expandResList.append(tmpExpandRes)
        resList += expandResList
        return resList


def createDictTable(conn: connector.MySQLConnection):
    '''
    创建 wordDict 表
    '''
    cursor = conn.cursor()
    cursor.execute("create table %s (%s %s, %s %s, %s %s, %s %s, PRIMARY KEY(%s))" % (
        dictTableName, dictTableCols[0][0], dictTableCols[0][1], dictTableCols[1][0],
        dictTableCols[1][1], dictTableCols[2][0], dictTableCols[2][1], dictTableCols[3][0], dictTableCols[3][1], dictTableCols[0][0]))
    cursor.close()


def write2db(resList: list, conn: connector.MySQLConnection):
    '''
    将resList中的数据插入到数据库 reader_hp 的 wordDict 表
    数据格式 {"word": xxx, "phonetic": xxx, "translation": xxx, "exchange": xxx}
    '''
    cursor = conn.cursor()
    i = 0
    for res in resList:
        if i % 10000 == 0:
            print("insert: " + str(i / 10000), file=sys.stderr)
        i += 1
        for key in res.keys():
            res[key] = res[key].replace('"', '\\"')
        tmps = 'insert into %s values("%s", "%s", "%s", "%s");' % (
            dictTableName, res["word"], res["phonetic"], res["translation"], res["exchange"])
        cursor.execute(tmps)
    print("cursor rowcount" + str(cursor.rowcount))
    conn.commit()
    cursor.close()


def statistic(resList: list):
    '''
    统计单词中 translation 字段的最大长度
    '''
    print("res line num: " + str(resList.__len__()))
    maxTransLen = 0
    for res in resList:
        maxTransLen = max(maxTransLen, res["translation"].__len__())
    print("max translation len: " + str(maxTransLen))


def checkAllWord(resList: list):
    '''
    将所有word输出到文件中
    '''
    wordList = []
    for res in resList:
        wordList.append(res["word"] + "\n")
    wordList.sort()
    with open("tmp.txt", "w", encoding="utf-8") as fp:
        fp.writelines(wordList)


def parseDictAndMakeTable(conn: connector.MySQLConnection):
    '''
    从ecdit.csv读取数据，创建表，并将数据导入到数据库
    '''
    createDictTable(conn)
    resList = process()
    random.shuffle(resList)
    write2db(resList, conn)


if __name__ == "__main__":
    # resource.setrlimit(resource.RLIMIT_DATA, resource.RLIM_INFINITY, resource.RLIM_INFINITY)
    conn = connector.connect(user="root", password="123456", database=dbName)
    parseDictAndMakeTable(conn)
    conn.close()
