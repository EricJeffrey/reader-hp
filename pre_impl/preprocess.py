'''
预处理文本
'''

import json


def ht_txt2json():
    '''
    将 txt格式的英文版HP转换为json文件
    '''
    res = {"title": "", "chapterCount": 0, "chapters": []}
    with open("tmp.txt", "r", encoding="utf-8") as rfp:
        lines = rfp.readlines()
        res["title"] = lines[0]
        chapindexes = []
        for i in range(1, len(lines)):
            if lines[i][0:7] == "CHAPTER":
                chapindexes.append(i)
        chapindexes.append(len(lines) + 1)
        res["chapterCount"] = len(chapindexes) - 1
        for i in range(0, len(chapindexes) - 1):
            tmpchapter = {
                "title": lines[chapindexes[i] + 1], "lineCount": chapindexes[i + 1] - chapindexes[i] - 2, "lines": []}
            for j in range(chapindexes[i] + 2, chapindexes[i + 1]):
                if j < len(lines):
                    tmpchapter["lines"].append(lines[j])
            res["chapters"].append(tmpchapter)
        json.dump(res, open("tmpp.json", "w", encoding="utf-8"))

if __name__ == "__main__":
    ht_txt2json()