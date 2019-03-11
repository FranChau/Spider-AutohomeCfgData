# -*- coding:utf-8 -*-
# author  : Fran_Chau
# datetime: 2019/3/8

import json, xlwt
import os, re, time

'''
第七步读取数据文件，生成excel
'''


class ExtractData(object):
    def __init__(self):
        self.startRow = 0
        self.isFlag = True
        self.workbook = xlwt.Workbook(encoding='ascii')  # 创建一个文件
        self.worksheet = self.workbook.add_sheet('汽车之家')  # 创建一个表

    def readFile(self, file):
        # 读取文件
        path = r"./data/jsonNew/"
        with open(path + file, "r", encoding="utf-8") as f:
            print("read file ", file)
            return f.read()

    def extractData(self, text, file):
        # 渲染js,返回renderData
        # global isFlag, startRow  # 默认记录表头
        carItem = {}
        # 解析基本参数配置参数，颜色三种参数，其他参数
        configRe = re.findall("var config = (.*?);", text)
        optionRe = re.findall("var option = (.*?);var", text)
        bagRe = re.findall("var bag = (.*?);", text)
        # config = configRe[0] if configRe else ""
        # option = optionRe[0] if optionRe else ""
        # bag = bagRe[0] if bagRe else ""

        try:
            config = json.loads(configRe[0])
            option = json.loads(optionRe[0])
            bag = json.loads(bagRe[0])
            print("config: ", config)
            print("option: ", option)
            print("bag: ", bag)

            configItem = config['result']['paramtypeitems'][0]['paramitems']
            optionItem = option['result']['configtypeitems'][0]['configitems']

            # 解析基本参数
            for car in configItem:
                carItem[car['name']] = []
                for ca in car['valueitems']:
                    carItem[car['name']].append(ca['value'])

            # 解析配置参数
            for car in optionItem:
                carItem[car['name']] = []
                for ca in car['valueitems']:
                    carItem[car['name']].append(ca['value'])
            if self.isFlag:
                co1s = 0
                for co in carItem:
                    co1s += 1
                    self.worksheet.write(self.startRow, co1s, co)
                else:
                    self.startRow += 1
                    self.isFlag = False

            # 计算起止行号
            endRowNum = self.startRow + len(carItem['车型名称'])  # 车辆款式记录数
            for row in range(self.startRow, endRowNum):
                print(row)
                colNum = 0
                for col in carItem:
                    colNum += 1
                    print(str(carItem[col][row - self.startRow]), end='|')
                    self.worksheet.write(row, colNum, str(carItem[col][row - self.startRow]))
            else:
                self.startRow = endRowNum
        except:
            # f = open(r"./data/exception.txt", "a", encoding="utf-8")
            with open(r"./data/exception.txt", "a", encoding="utf-8") as f:
                f.write(file.title() + "\n")

    def main(self):
        files = os.listdir(r"./data/jsonNew/")
        for file in files:
            text = self.readFile(file)
            self.extractData(text, file)
        filepath = r"./data/AutohomeConfigInfo.xls"
        self.workbook.save(filepath)


if __name__ == '__main__':
    start = time.time()
    ExtractData().main()
    print("\n耗时： ", time.time() - start)
