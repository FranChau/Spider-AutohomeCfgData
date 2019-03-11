# -*- coding:utf-8 -*-
# author  : Fran_Chau
# datetime: 2019/3/8

import re, os, time
import asyncio, aiofiles

'''
第二步，解析出每个车型的关键js并加上js执行头代码
asyncio, aiofiles使用教程:https://blog.csdn.net/zv3e189os5c0tsknrbcl/article/details/80906206
'''


class GetJS(object):
    def __init__(self):
        pass

    async def readFile(self, fileName):
        '''读取html文件'''
        async with aiofiles.open("./data/html/" + fileName, "r", encoding="utf-8") as f:
            print("read file ", fileName)
            return await f.read()

    async def saveFile(self, newHtml, fileName):
        '''保存为新的html文件'''
        path = r"./data/alljs/"
        if not os.path.exists(path):
            os.makedirs(path)
        async with aiofiles.open(path + fileName, "w", encoding="utf-8") as f:
            print("write file ", fileName)
            await f.write(newHtml)

    async def getJS(self, fileName):
        alljs = ("var rules = '2';"
                 "var document = {};"
                 "function getRules(){return rules}"
                 "document.createElement = function() {"
                 "      return {"
                 "              sheet: {"
                 "                      insertRule: function(rule, i) {"
                 "                              if (rules.length == 0) {"
                 "                                      rules = rule;"
                 "                              } else {"
                 "                                      rules = rules + '#' + rule;"
                 "                              }"
                 "                      }"
                 "              }"
                 "      }"
                 "};"
                 "document.querySelectorAll = function() {"
                 "      return {};"
                 "};"
                 "document.head = {};"
                 "document.head.appendChild = function() {};"

                 "var window = {};"
                 "window.decodeURIComponent = decodeURIComponent;")
        print("parse file ", fileName)
        text = await self.readFile(fileName)
        try:
            js = re.findall('(\(function\([a-zA-Z]{2}.*?_\).*?\(document\);)', text)
            for item in js:
                alljs += item
        except Exception as e:
            print(e)

        newHtml = "<html><meta http-equiv='Content-Type' content='text/html; charset=utf-8' /><head></head><body>    <script type='text/javascript'>"
        alljs = newHtml + alljs + " document.write(rules)</script></body></html>"
        await self.saveFile(alljs, fileName)

    def main(self):
        files = os.listdir("./data/html")
        loop = asyncio.get_event_loop()
        tasks = [asyncio.ensure_future(self.getJS(file)) for file in files]
        tasks = asyncio.gather(*tasks)
        loop.run_until_complete(tasks)


if __name__ == '__main__':
    start = time.time()
    GetJS().main()
    print("耗时： ", time.time() - start)
