'''
单词 句子记录数据库表的创建
'''
import mysql.connector as connector

dbName = "reader_hp"

wordRectTableName = "wordRecord"
wordRecTableCols = [
    ['word', 'varchar(255) BINARY'],
    ['phonetic', 'varchar(255)'],
    ['translation', 'varchar(1000)'],
    ['exchange', 'varchar(255)'],
]

sentenceRecTableName = "sentenceRecord"
sentenceRecTableCols = [
    ['id', 'INT UNSIGNED AUTO_INCREMENT'],
    ['sentence', 'MEDIUMTEXT']
]


def createWordRecTable(conn: connector.MySQLConnection):
    '''
    创建 wordRecord 表
    '''
    cursor = conn.cursor()
    cursor.execute("create table %s (%s %s, %s %s, %s %s, %s %s, PRIMARY KEY(%s))" % (
        wordRectTableName,
        wordRecTableCols[0][0], wordRecTableCols[0][1],
        wordRecTableCols[1][0], wordRecTableCols[1][1],
        wordRecTableCols[2][0], wordRecTableCols[2][1],
        wordRecTableCols[3][0], wordRecTableCols[3][1],
        wordRecTableCols[0][0]))
    cursor.close()


def createSentenceRecTable(conn: connector.MySQLConnection):
    '''
    创建 sentenceRecord 表
    '''
    cursor = conn.cursor()
    cursor.execute("create table %s (%s %s, %s %s, PRIMARY KEY(%s))" % (
        sentenceRecTableName,
        sentenceRecTableCols[0][0], sentenceRecTableCols[0][1],
        sentenceRecTableCols[1][0], sentenceRecTableCols[1][1],
        sentenceRecTableCols[0][0]))
    cursor.close()


if __name__ == "__main__":
    conn = connector.connect(user="root", passwd="123456", database=dbName)
    createWordRecTable(conn)
    createSentenceRecTable(conn)
