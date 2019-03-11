# Spider-AutohomeCfgData
Crawl all the car configuration data on the AutoHome website
# 爬取汽车之家所有车型的参数配置

汽车之家直接在HTML抓取参数配置的数据是不完整的，原因是因为一些数据字体是通过JS混淆加密渲染出来的。\
网上已经有很多汽车之家相关的爬取教程，本人这次主要借鉴[康仔](https://www.cnblogs.com/kangz/p/10011348.html)这篇文章的思路实现，在这里也感谢他的分享。由于爬虫的效率是一大关键点，故本人在借鉴代码的时候也对代码进行了优化，使用asyncio,aiohttp实现协程异步请求网页，由于数据保存在本地，故使用aiofiles实现异步读取文件。
后期考虑加入多进程进行优化。

*从 Python 3.4 开始，Python 中加入了协程的概念，但这个版本的协程还是以生成器对象为基础的，在 Python 3.5 则增加了 async/await，使得协程的实现更加方便。asyncio库能很便捷的实现协程异步，常与aiohttp库配合使用，实现异步请求。*

## 思路：共分为五大步骤实现：

### 1. 抓取全站车型参数配置  *getAllHtml.py*

使用aiohttp, asyncio异步抓取所有车型的网页，保存到本地。

### 2. 解析出每个车型的关键js并加上js执行头代码 *getJS.py*

从HTML文档里提取JS加密相关的代码，并加上一段HTML组成新的HTML文档。

### 3. 解析出每个车型的数据json，保存到本地。*getDataJson.py*

### 4. 渲染步骤2的JS代码，得到字典集和对应标位，并在步骤3中将对应标位的<span>标签替换为内容

使用js2py渲染js，发现渲染速度相比 Chrome('--headless') 慢很多，这里使用 Chrome('--headless') 渲染JS

### 5. 提取数据，保存为xls文件*AutohomeConfigInfo.xls*

由于有些车型没有配置参数，故将这些车型的ID记录在*exception*文件中

## 结果：
总共爬取8938个车型的配置参数的数据，耗时52分钟

代码是在咱6年的笔记本上跑的，可谓是老牛了， **i5三代+4G**


***本人目前还处于技术学习阶段，接触爬虫不久，全是自学，目前处于边学习边找工作状态，此项目为练手项目，请勿商用。***

***如广大网友有高明之见，欢迎指点！也希望能结交更多大牛，一起成长！***





