#!coding:utf-8
#微信接口
from django.shortcuts import render,HttpResponse
import json
import urllib
import time
import hashlib
# appid appsecrety

class Wx():
    _APPID = 'wxd6d7a9d754b8b88c'
    _APPS='7532acbce2d5efa153b2cf3a066ed443'
    _TOKEN = {"time":"","token":""}


    # 第一次验证
    @classmethod
    def check(cls,request):
        # 与微信验证
        # 将timestamp，noce，token按字典排序
        
        timestamp = request.GET.get('timestamp')
        nonce     = request.GET.get('nonce')
        taken     = "dangweiwu"
        signature = request.GET.get('signature')
        echostr   = request.GET.get("echostr","") 
        
        # 排序后进行sha1加密
        l = sorted([timestamp,nonce,taken])
        tmpstr = "".join(l)

        tmpstr = hashlib.sha1(tmpstr).hexdigest()
        
        if signature == tmpstr and echostr:
            # 验证成功返回echostr
            return HttpResponse(echostr)
        

    # 获取token
    @classmethod
    def getToken(cls):
        # 判断文件是否存在
        if cls._TOKEN['token']:
            if int(time.time())-int(TOKEN['time'])<7000:
                return cls._TOKEN['token']


        # wx token获取
        url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (cls._APPID,cls._APPS)
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



    @classmethod
    def getIp(cls):
        token = cls.getToken()
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



    # 文本回复
    # @parameter
    # toUser:接受者
    # fromUser：发送者
    # creatTime：创建时间戳
    # mysgType：发送类型 “text”
    # content：发送内容
    # 返回xml数据

    @classmethod
    def xmlText(cls,toUser,fromUser,creatTime,content,msgType='text'):
        template = """<xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%s</CreateTime>
        <MsgType><![CDATA[%s]]></MsgType>
        <Content><![CDATA[%s]]></Content>
        </xml>"""%(toUser,fromUser,creatTime,msgType,content)
        return HttpResponse(template,content_type="application/xml")

    # 文本回复简化版
    # 参数：
    # root：微信发送请求的xml数据
    # content：发送内容utf-8格式
    @classmethod
    def responseText(cls,root,content):
        toUser = root.find("FromUserName").text
        fromUser = root.find('ToUserName').text
        creatTime = str(int(time.time()))
        msgType = 'text'
        content = content
        return cls.xmlText(toUser,fromUser,creatTime,msgType,content)

    # 图片文本
    @classmethod
    def creatNew(cls,title,description,picurl,url):
        new={
        "title":title,
        'description':description,
        'picurl':picturl,
        'url':url,
        }

        return new



    @classmethod
    def xmlNews(cls,root,news_list):

        # 获取请求xml信息
        toUser = root.find("FromUserName").text
        fromUser = root.find('ToUserName').text
        creatTime = str(int(time.time()))

        # xml数据组装
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

