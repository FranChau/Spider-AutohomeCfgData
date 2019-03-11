# -*- coding:utf-8 -*-
# author  : Fran_Chau
# datetime: 2019/3/8

import re, os, time
import asyncio, aiofiles

'''
第三步 解析出每个车型的数据json，保存到本地。
'''


class GetDataJson(object):
    def __init__(self):
        pass

    async def readFile(self, fileName):
        # 读取html文件
        async with aiofiles.open("./data/html/" + fileName, "r", encoding="utf-8") as f:
            print("read file ", fileName)
            return await f.read()

    async def saveFile(self, newHtml, fileName):
        # 另存为文件
        path = r"./data/json/"
        if not os.path.exists(path):
            os.makedirs(path)
        async with aiofiles.open(path + fileName, "w", encoding="utf-8") as f:
            print("write file ", fileName)
            await f.write(newHtml)

    async def getData(self, fileName):
        # 解析数据的json
        print("parse file ", fileName)
        text = await self.readFile(fileName)
        jsonData = ""
        config = re.search('var config = (.*?){1,};', text)
        if config != None:
            print(config.group(0))
            jsonData += config.group(0)
        option = re.search('var option = (.*?)};', text)
        if option != None:
            print(option.group(0))
            jsonData += option.group(0)
        bag = re.search('var bag = (.*?);', text)
        if bag != None:
            print(bag.group(0))
            jsonData += bag.group(0)
        await self.saveFile(jsonData, fileName)

    def main(self):
        files = os.listdir("./data/html/")
        loop = asyncio.get_event_loop()
        tasks = [asyncio.ensure_future(self.getData(file)) for file in files]
        tasks = asyncio.gather(*tasks)
        loop.run_until_complete(tasks)


if __name__ == '__main__':
    start = time.time()
    GetDataJson().main()
    print("耗时： ", time.time() - start)
