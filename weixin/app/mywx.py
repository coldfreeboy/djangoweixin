#!coding:utf-8
#微信接口
from django.shortcuts import render,HttpResponse
import json,time,os,hashlib
import urllib,urllib2
import requests


# token写入文件或者读取
def _F(name,data=""):
    file = os.path.exists(name)
    if not file and not data:
        return ""

    if data:
        with open(name,"wb") as f:
            f.write(json.dumps(data))

    if not data:
        with open(name,"rb") as f:
            d  = f.read()
            return json.loads(d)


# 微信类模块
class Wx():
    _APPID = 'wxd6d7a9d754b8b88c'
    _APPS='7532acbce2d5efa153b2cf3a066ed443'
    

    def __init__(self):
        print "class init"


    # 第一次验证
    @classmethod
    def check(cls,request):
        # 与微信验证
        # 将timestamp，noce，token按字典排序
        
        timestamp = request.GET.get('timestamp')
        nonce     = request.GET.get('nonce')
        # 根据自己情况设置
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
        d = _F("mytoken.cach")
        if d:
            if time.time()-int(d['time'])<7000:
                return d['token']


        # wx token获取
        url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (cls._APPID,cls._APPS)
        response = urllib.urlopen(url)
        jsondata = response.read()

        try:
            data = json.loads(jsondata)
        except:
            sys.exit()

        if data["access_token"]:
 
            jd={}
            jd['time']=int(time.time())
            jd['token']=data["access_token"]
            # print(data['access_token'])
            _F('mytoken.cach',jd)
            return data['access_token']

        return ""


        # 获取ip
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



    # 基本文本回复
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

    # 简化版文本回复
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
        return cls.xmlText(toUser,fromUser,creatTime,content,msgType)

    # 图片文本
    # 创建item内容
    @classmethod
    def createNew(cls,title,description,picurl,url):
        new={
        "title":title,
        'description':description,
        'picurl':picurl,
        'url':url,
        }

        return new


    # 创建图片文本响应
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

    # 创建按钮
    @classmethod
    def createBtn(cls,btn_conf):
        if type(btn_conf) != dict:
            return "请输入字典类型参数"

        json_data = json.dumps(btn_conf,ensure_ascii=False)

        access_token = cls.getToken()
        url="https://api.weixin.qq.com/cgi-bin/menu/create?"

        get_data = urllib.urlencode({"access_token":access_token})

        url ="%s%s" %(url,get_data)

        req = urllib2.Request(url)  

        req.add_header('Content-Type', 'application/json')

        req.add_header('encoding', 'utf-8')  

        response = urllib2.urlopen(req, json_data)  

        result = response.read()

        return result

    # 上传图片
    @classmethod
    def curl_file(cls,img_path,file_type,file_name,content_type):
        # Content-Disposition: form-data; name="file"; filename="sygj.png"
        # Content-Type: image/png
        file_types=['image','thumb','video','voice']
        if file_type not in file_types:
            return {'error':1,'msg':"文件类型不对"}

        if not os.path.exists(img_path):
            return {'error':1,'msg':"文件不存在"}

        image =open(img_path,'rb')
        url = 'https://api.weixin.qq.com/cgi-bin/media/upload?'
        get_data = urllib.urlencode({"access_token":cls.getToken(),"type":file_type})
        url = "%s%s" % (url,get_data)

        file = {
        file_type :(file_name,image,content_type)
        }

        response = requests.post(url,files=file)

        image.close()
        return {'error':0,'msg':response.content}







