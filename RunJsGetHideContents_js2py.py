# -*- coding:utf-8 -*-
# author  : Fran_Chau
# datetime: 2019/3/8

'''
使用js2py渲染js，发现渲染速度相比 Chrome('--headless') 较慢
'''

import js2py
import asyncio, aiofiles
import os, time, re

async def readFile(filePath):
    # 读取文件
    async with aiofiles.open(filePath, "r", encoding="utf-8") as f:
        print("read file ", filePath)
        return await f.read()


async def saveFile(newHtml, fileName):
    # 另存为文件
    path = r"./data/jsonNew/"
    if not os.path.exists(path):
        os.makedirs(path)
    async with aiofiles.open(path + fileName, "w", encoding="utf-8") as f:
        print("write file ", fileName)
        await f.write(newHtml)


async def jsRendering(fileName):
    # 使用js2py渲染js,返回renderData
    jsFilePath = "./data/alljs/" + fileName
    data = await readFile(jsFilePath)
    js = js2py.EvalJs()
    js.execute(data)
    renderData = js.eval("rules")
    print("Js Rendered:  ",renderData)
    return renderData

async def replaceSpan(fileName):
    # 读取json数据，替换<span>标签的内容
    renderData = await jsRendering(fileName)
    jsonPath = "./data/json/" + fileName
    json = await readFile(jsonPath)
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
    print(json)
    await saveFile(json, fileName)


if __name__ == '__main__':
    start = time.time()
    files = os.listdir("./data/html/")

    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(replaceSpan(file)) for file in files]
    tasks = asyncio.gather(*tasks)
    loop.run_until_complete(tasks)

    print("耗时： ", time.time() - start)

