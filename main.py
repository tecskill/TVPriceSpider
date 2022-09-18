from urllib import request
import re
import time
import random
import csv
from ua_info import ua_list
import itertools
import os

import GlobalDefine as GDefine
# 定义一个爬虫类
class HitesSpider(object):
    # 初始化
    # 定义初始页面url
    # reference: http://c.biancheng.net/python_spider/
    def __init__(self, listBrandName):
        self.listSearchBrand = listBrandName
        self.url = 'https://www.hites.com/busqueda?q={}&start=0&sz=48'

    def extract_Modle_Size(self, paraStr):
        # string like : 'Led TCL 55P725 / 55  / Ultra HD / 4K / Smart Tv'
        strFix = '/'
        b = paraStr.find(strFix)
        if(b > 0):
            c = paraStr[:b]
            listStr = c.split()
            modelStr = listStr[-1]
            listStr = paraStr[b+len(strFix):].split()
            sizeStr = ''.join([ch for ch in listStr[0] if ch.isdigit()])
            return modelStr, sizeStr
        else:
            return '', ''

    # 请求函数
    def get_html(self, url):
        headers = {'User-Agent': random.choice(ua_list)}
        req = request.Request(url=url, headers=headers)
        res = request.urlopen(req)
        html = res.read().decode()
        # 直接调用解析函数
        return html

    # 解析函数
    def parse_html(self, html:str):
        # 正则表达式
        re_bds = '<div class="product-tile-body">.*?href="(.*?)".*?action&quot;:&quot;(.*?)&quot;.*?<span class="value" content="(.*?)"'
        # 生成正则表达式对象
        pattern = re.compile(re_bds, re.S)
        r_list = pattern.findall(html)
        return r_list


    # 保存数据函数，使用python内置csv模块
    def save_html(self, brandName:str, r_list, fileSaveName:str):
        savePath = fileSaveName + '.csv'
        bSaveHead = 0
        if(os.path.exists(savePath) == 0):
            bSaveHead = 1
        # 生成文件对象
        with open(savePath, 'a', newline='', encoding="utf-8") as f:
            # 生成csv操作对象
            writer = csv.writer(f)
            if(bSaveHead > 0):
                # 写 cvs标题行
                title = GDefine.SaveTilleList
                writer.writerow(title)
            # 整理数据
            for r in r_list:
                html = r[0]
                desc = r[1]
                #price = str(round(float(r[2])/1000,3))
                price = r[2]
                modle, size = self.extract_Modle_Size(desc)
                L = [brandName, size, modle, desc, price, html]
                # 写入csv文件
                writer.writerow(L)
                print(brandName, modle, desc, price)

    # 主函数
    def run(self):
        saveName = 'PriceSpider_'+'hites_com'
        for brandName in self.listSearchBrand:
            #获取网页地址
            url = self.url.format(brandName)
            # 抓取网页内容
            htmlContent = self.get_html(url)
            # 解析目标内容
            listPrice = self.parse_html(htmlContent)
            # 保存数据
            self.save_html(brandName, listPrice, saveName)
            # 生成1-2之间的浮点数
            time.sleep(random.uniform(1, 2))



# 以脚本方式启动
if __name__ == '__main__':
    # 捕捉异常错误
    searchList = ['TCL+TV', 'LG+TV', 'SAMSUNG+TV', 'PHILIPS+TV','HISENSE+TV', 'MASTER-G+TV', 'XIAOMI+TV']
    try:
        spider = HitesSpider(searchList)
        spider.run()
    except Exception as e:
        print("错误:", e)