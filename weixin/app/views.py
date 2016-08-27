#!coding:utf-8
from django.shortcuts import render,HttpResponse
import hashlib
import xml.etree.cElementTree as ET
import time
import urllib,urllib2
from django.views.decorators.csrf import csrf_exempt
import json
import sys
import os
import urllib2
from mywx import Wx


def post_file():
  pass

def creat_btn():


    data_b = {
         "button":[
         {  
              "type":"click",
              "name":"主页",
              "key":"2",
          },
          {
               "name":"菜单",
               "sub_button":[
               {    
                   "type":"view",
                   "name":"百度",
                   "url":"http://www.baidu.com",
                },
                {
                   "type":"click",
                   "name":"随机",
                   "key":"suiji",
                },
                {
                   "type":"click",
                   "name":"news",
                   "key":"1",
                }]
           }]
    }


    json_data = json.dumps(data_b,ensure_ascii=False)

    access_token = getToken()
    url="https://api.weixin.qq.com/cgi-bin/menu/create?"

    get_data = urllib.urlencode({"access_token":access_token})

    url ="%s%s" %(url,get_data)

    req = urllib2.Request(url)  

    req.add_header('Content-Type', 'application/json')

    req.add_header('encoding', 'utf-8')  

    response = urllib2.urlopen(req, json_data)  

    result = response.read()

    return result

btn ={
         "button":[
         {  
              "type":"click",
              "name":"主页",
              "key":"1",
          },
          {
               "name":"菜单",
               "sub_button":[
               {    
                   "type":"view",
                   "name":"百度",
                   "url":"http://www.baidu.com",
                },
                {
                   "type":"click",
                   "name":"随机",
                   "key":"2",
                },
                {
                   "type":"click",
                   "name":"news",
                   "key":"2",
                }]
           }]
    }
    

# Create your views here.
def home(request):
    # return HttpResponse(Wx.test())

    token = Wx.getToken()
    print(token)
    token = Wx.getToken()
    print(token)
    return HttpResponse(token)

    # if token:
    #     ips = getIp(token)

    #     if ips:
    #         print(ips)
    #         print(type(ips))
    #         return HttpResponse(ips)
    #     else:
    #         return HttpResponse("error")    

    # 创建菜单
    # data = Wx.createBtn(btn)
    # 上传图片

    # res = Wx.curl_file("xin.png",'image','xim.png',"image/png")
    # if res['error']:
    #     return HttpResponse(res['msg'])
    # else:
    #     msg = res['msg']

    #     with open('imageMsg.txt','wb') as f:
    #         f.write(msg)
    #     return HttpResponse(msg)


    # return HttpResponse(data)

    # return render(request,"test.html")


# 文本回复
def responseText(root):

    # toUser = root.find("FromUserName").text
    # fromUser = root.find('ToUserName').text
    # creatTime = str(int(time.time()))
    # msgType = 'text'

    context = root.find('Content').text

    if context.find("介绍".decode('utf-8')) != -1 :
        content = "全栈开发，bae部署，经济实惠。"
        
    elif context == "1":
        content = "<a href='https://www.taobao.com/'>淘宝</a> "
        
    elif context == "2":
        news_list =[]

        one =  Wx.createNew("百度",'百度链接',
            'https://ss0.baidu.com/6ONWsjip0QIZ8tyhnq/it/u=2306836341,4091540152&fm=58&s=39C718720E8EBE011B398BAC0300F024','http://www.baidu.com')
        news_list.append(one)
        news_list.append(one)

        return Wx.xmlNews(root,news_list)
    else:
        content="""说明页
----------
0:介绍测试 
1:淘宝链接测试
2:图片文章测试

第0项输入介绍
其余项输入对应数字
其他输入返回本页

"""
    return Wx.responseText(root,content)



# 菜单点击事件
def eventClick(root):
    key = root.find("EventKey").text
    if not key:
        return 0
    else:
        if key == "1":
            content = "key is 1 and menu is news"
            return Wx.responseText(root,content)
        if key =="2":
            content = "key is 2 and menu is 主页"
            return Wx.responseText(root,content)

@csrf_exempt
def index(request):
    # 微信验证
    if request.method == "GET":
        return Wx.check(request)

    # post接受到xml事件
    if request.method == "POST":

        tree = request.body
        if tree:
            root = ET.fromstring(tree)
        else:
            return HttpResponse('xml不能解析')

        #事件
        if root.find('MsgType').text.lower() == "event":
            # 关注事件
            if root.find('Event').text.lower() == 'subscribe':
                return Wx.responseText(root,"欢迎订阅")
            if root.find('Event').text.lower() == 'click':
                return eventClick(root)

        # 文本
        if root.find('MsgType').text.lower() == "text":
            return responseText(root)


        

    






    
    

