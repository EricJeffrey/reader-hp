'''
测试数据库的可用性，主要针对字典数据库
'''

import mysql.connector as connector

dbName = 'reader_hp'
dictTableName = 'wordDict'


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


def testWordsQuery(conn: connector.MySQLConnection):
    '''
    测试字典的可用性，适当验证正确性
    '''
    wordlist = ['this', 'method', 'retrieves', 'the', 'next', 'n2e', 'row', 'of', 'a', 'query',
                'result', 'set', 'and', 'returns', 'a', 'single', 'sequence', 'or', 'none',
                'if', 'no', 'more', 'rows', 'are', 'available', 'by', 'default', 'the',
                'returned', 'tuple', 'consists', 'of', 'data', 'returned', 'by', 'the',
                'server', 'converted', 'to', 'python', 'objects', "tuple'sdf",
                "select count(word) from wordDict", 'xsadgk,dasg', 'cornflower', 'long time ago']
    for word in wordlist:
        print("%s -->  %s" % (word, queryWord(word, conn)))


if __name__ == "__main__":
    conn = connector.connect(user='root', passwd='123456', database=dbName)
    testWordsQuery(conn)
