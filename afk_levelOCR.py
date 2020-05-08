# encoding:utf-8
import base64
import requests
import os
import re
from lxml import html
# @Author  : Saberpan

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
}
class SpiderTieba():
    #解析网页,输入xpath参数，返回需要的值
    def analysis(self,url,xpath):
        #返回网页
        rs = requests.get(url,headers=headers).text
        #生成etree
        etree = html.etree
        #解析网页
        html1 = etree.HTML(rs)
        xpath1 = html1.xpath(xpath)
        return xpath1

    #爬取图片
    def takephoto(self,url,dirname,xpath="//li[@class='l_reply_num'][1]/span[2]/text()"):
        #获取总页数
        page = SpiderTieba().analysis(url,xpath)
        #翻页爬取
        for i in range(1,int(page[1])+1):
            print(f'爬取第{i}页的图片')
            url2 = f'{url}?pn={i}'
            photo = SpiderTieba().analysis(url2, "//img[@class='BDE_Image']/@src")
            for i in photo:
                image_link = requests.get(i)
                image = image_link.content
                print(i)
                #当前目录下新建文件夹
                # dirpath = os.getcwd() + '/afk-25(矹呐咔叽哈)'
                #D盘新建文件夹
                dirpath = 'D:/'+ dirname
                if not os.path.isdir(dirpath):
                    os.makedirs(dirpath)
                imagename = i[-14:]
                print(f'正在下载{imagename}')
                a = open(dirpath+'/'+imagename,'wb')
                a.write(image)
                a.close()

class SpiderTaptap():
    def takephoto(self,url,dirname):
        #get imageurl
        imageurl = SpiderTieba().analysis(url,'//img[@class="bbcode-img"]/@data-origin-url')
        for i in imageurl:
            image= requests.get(i).content
            imagename = i[-11:]
            imgpath = 'D:\\'+dirname
            if not os.path.isdir(imgpath):
                os.makedirs(imgpath)
                print('创建路径完毕')
            imgfile = open(imgpath+'/'+imagename, 'wb')
            imgfile.write(image)
            imgfile.close()
            print('已完成'+imagename)

# client_id 为官网获取的AK， client_secret 为官网获取的SK
def get_token():
    host = ''
    response = requests.get(host)
    rsjson = response.json()
    access_token = rsjson['access_token']
    # print(access_token)
    return access_token

def get_imagename(imagepath):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/webimage"
    # 二进制方式打开图片文件
    f = open(imagepath, 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    access_token = get_token()
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        # print(response.json())
        try:
            original = response.json()
            filename = '关卡'+re.findall(r"关卡(.+?)'",str(original))[0]
            print('识别成功'+filename)
            return filename
        except Exception:
            print('识别失败')
            return imagepath[-14:-4]

def get_finalimg(dirname):
    dirpath = "D:\\"+dirname
    imglist = os.listdir(dirpath)
    for i in imglist:
        try:
            imgpath = dirpath+'\\'+i
            print('图片地址'+imgpath)
            imgname = get_imagename(imgpath)
            newname = dirpath+'\\'+str(imgname)+'.jpg'
            print('新地址'+newname)
            os.rename(imgpath,newname)
        except Exception:
            pass


url = 'https://tieba.baidu.com/p/6569989146'
dirname = 'afk-24(那个人是谁啊)'
SpiderTieba().takephoto(url=url,dirname=dirname)
# SpiderTaptap().takephoto(url=url,dirname=dirname)
get_finalimg(dirname=dirname)
