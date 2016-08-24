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

APPID = 'wxd6d7a9d754b8b88c'
APPS='7532acbce2d5efa153b2cf3a066ed443'


TOKEN = {"time":"","token":""}

def getToken():
    # 判断文件是否存在
    if TOKEN['token']:
        if int(time.time())-int(TOKEN['time'])<7100:
            return TOKEN['token']


    # wx token获取
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (APPID,APPS)
    response = urllib.urlopen(url)
    jsondata = response.read()

    try:
        data = json.loads(jsondata)
    except:
        sys.exit()

    if data["access_token"]:
        TOKEN['time']=int(time.time())
        TOKEN['token']=data["access_token"]
        # print(data['access_token'])
        return data['access_token']

    return ""

def getIp(token):
    url = "https://api.weixin.qq.com/cgi-bin/getcallbackip?access_token=%s" % token

    response = urllib.urlopen(url)
    jsondata = response.read()

    try:
        data = json.loads(jsondata)
    except:
        sys.exit()

    if data['ip_list']:
        return data['ip_list']

    return ""

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
    # url =  "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % access_token
    url="https://api.weixin.qq.com/cgi-bin/menu/create?"

    get_data = urllib.urlencode({"access_token":access_token})

    url ="%s%s" %(url,get_data)



    print(url)
    print(json_data)
    
    req = urllib2.Request(url)  

    req.add_header('Content-Type', 'application/json')

    req.add_header('encoding', 'utf-8')  

    response = urllib2.urlopen(req, json_data)  

    result = response.read()

    return result


    

# Create your views here.
def home(request):
    return HttpResponse(Wx.test())

    # token = getToken()
    # print(token)

    # if token:
    #     ips = getIp(token)

    #     if ips:
    #         print(ips)
    #         print(type(ips))
    #         return HttpResponse(ips)
    #     else:
    #         return HttpResponse("error")    

    data = creat_btn()

    return HttpResponse(data)

    return render(request,"test.html")

# 获取token



# def xmlText(toUser,fromUser,creatTime,msgType,content):
#     template = """<xml>
#     <ToUserName><![CDATA[%s]]></ToUserName>
#     <FromUserName><![CDATA[%s]]></FromUserName>
#     <CreateTime>%s</CreateTime>
#     <MsgType><![CDATA[%s]]></MsgType>
#     <Content><![CDATA[%s]]></Content>
#     </xml>"""%(toUser,fromUser,creatTime,msgType,content)
#     return HttpResponse(template,content_type="application/xml")

def xmlNews(root):
    toUser = root.find("FromUserName").text
    fromUser = root.find('ToUserName').text
    creatTime = str(int(time.time()))

    news_list = []
    obj_news={
    "title":"百度",
    'description':"百度链接",
    'picurl':"https://ss0.bdstatic.com/5aV1bjqh_Q23odCf/static/superman/img/logo/logo_white_fe6da1ec.png",
    'url':'http://www.baidu.com'
    }
    obj_news2={
    "title":"百度",
    'description':"百度链接",
    'picurl':"https://ss0.bdstatic.com/5aV1bjqh_Q23odCf/static/superman/img/logo/logo_white_fe6da1ec.png",
    'url':'http://www.baidu.com'
    }

    news_list.append(obj_news)
    news_list.append(obj_news2)
    templates="<Articles>"
 
    for i in news_list:

        template ="""<item><Title><![CDATA[%s]]></Title> 
        <Description><![CDATA[%s]]></Description>
        <PicUrl><![CDATA[%s]]></PicUrl>
        <Url><![CDATA[%s]]></Url></item>""" % (i['title'],i['description'],i['picurl'],i['url'])

        templates = "%s%s" % (templates,template)

    templates = "%s</Articles>" % templates
    template_head ="""<xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[news]]></MsgType>
    <ArticleCount>%s</ArticleCount>""" % (toUser,fromUser,creatTime,len(news_list))
    template_body ="%s%s</xml>"%(template_head,templates)

    return HttpResponse(template_body,content_type="application/xml")



# # 关注响应
# def responseMsg(root):

#     toUser = root.find("FromUserName").text
#     fromUser = root.find('ToUserName').text
#     creatTime = str(int(time.time()))
#     msgType = 'text'
#     content = "欢迎订阅"

#     return xmlText(toUser,fromUser,creatTime,msgType,content)


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


        

    






    
    

