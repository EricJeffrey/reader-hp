
'''
获取所有句子，输出句子列表
'''

import mysql.connector as connector
import json


dbName = "reader_hp"
sentenceRecTableName = "sentenceRecord"
wordRecTableName = 'wordRecord'


def work():
    conn = connector.connect(user="root", passwd="123456", database=dbName)
    cursor = conn.cursor()
    cursor.execute("select sentence from %s" % (sentenceRecTableName))
    resList = cursor.fetchall()
    conn.close()
    retList = []
    for res in resList:
        retList.append({"sentence": res[0]})
    print(json.dumps(retList, ensure_ascii=False))


if __name__ == "__main__":
    work()
