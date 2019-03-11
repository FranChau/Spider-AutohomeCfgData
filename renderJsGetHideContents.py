# -*- coding:utf-8 -*-
# author  : Fran_Chau
# datetime: 2019/3/8

'''
使用js2py渲染js，发现渲染速度相比 Chrome('--headless') 较慢
这里使用 Chrome('--headless') 渲染JS
'''

import asyncio, aiofiles
import os, time, re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class RenderJsGetHideContents():
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options=self.chrome_options)

    async def readFile(self, filePath):
        # 读取文件
        async with aiofiles.open(filePath, "r", encoding="utf-8") as f:
            print("read file ", filePath)
            return await f.read()

    async def saveFile(self, newHtml, fileName):
        # 另存为文件
        path = r"./data/jsonNew/"
        if not os.path.exists(path):
            os.makedirs(path)
        async with aiofiles.open(path + fileName, "w", encoding="utf-8") as f:
            print("write file ", fileName)
            await f.write(newHtml)

    async def jsRendering(self, fileName):
        # 使用js2py渲染js,返回renderData
        path = "file:///" + os.getcwd() + "/data/alljs/"
        # path = r"file:///I:/01_Python_Workspace/AutohomeCfgData/data/alljs/"
        self.browser.get(path + fileName)
        text = self.browser.find_element_by_tag_name('body')
        renderData = text.text
        print("renderData ---> ", renderData)
        return renderData

    async def replaceSpan(self, fileName):
        # 读取json数据，替换<span>标签的内容
        renderData = await self.jsRendering(fileName)
        jsonPath = "./data/json/" + fileName
        json = await self.readFile(jsonPath)
        spans = re.findall("<span(.*?)></span>", json)
        for span in spans:
            # 获取class属性值,<span class='hs_kw15_configDQ'></span>
            sea = re.search("'(.*?)'", span)
            spanContent = str(sea.group(1)) + "::before { content:(.*?)}"
            # 在renderData匹配样式值
            spanContentRe = re.search(spanContent, renderData)
            if spanContentRe != None:
                if sea.group(1) != None:
                    print("匹配到的样式值=" + spanContentRe.group(1))
                    json = json.replace(str("<span class='" + sea.group(1) + "'></span>"),
                                        re.search("\"(.*?)\"", spanContentRe.group(1)).group(1))
        print("Replace JS-->", json)
        await self.saveFile(json, fileName)

    def main(self):
        files = os.listdir("./data/html/")

        loop = asyncio.get_event_loop()
        tasks = [asyncio.ensure_future(self.replaceSpan(file)) for file in files]
        tasks = asyncio.gather(*tasks)
        loop.run_until_complete(tasks)


if __name__ == '__main__':
    start = time.time()
    RenderJsGetHideContents().main()
    print("耗时： ", time.time() - start)
