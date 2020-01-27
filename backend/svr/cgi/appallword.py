
'''
获取所有单词，输出单词列表
'''

import mysql.connector as connector
import json


dbName = "reader_hp"
sentenceRecTableName = "sentenceRecord"
wordRecTableName = 'wordRecord'


def work():
    conn = connector.connect(user="root", passwd="123456", database=dbName)
    cursor = conn.cursor()
    cursor.execute("select * from %s" % (wordRecTableName))
    resList = cursor.fetchall()
    conn.close()
    retList = []
    for res in resList:
        retList.append({"word": res[0], "phonetic": res[1], "translation": res[2], "exchange": res[3]})
    print(json.dumps(retList, ensure_ascii=False))

if __name__ == "__main__":
    work()