#!coding:utf-8
from django.shortcuts import render,HttpResponse
import hashlib
import xml.etree.cElementTree as ET
import time
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request):
    return render(request,"test.html")


def xmlText(toUser,fromUser,creatTime,msgType,content):
    template = """<xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[%s]]></MsgType>
    <Content><![CDATA[%s]]></Content>
    </xml>"""%(toUser,fromUser,creatTime,msgType,content)
    return HttpResponse(template,content_type="application/xml")


# 关注响应时间
def responseMsg(root):

    toUser = root.find("FromUserName").text
    fromUser = root.find('ToUserName').text
    creatTime = str(int(time.time()))
    msgType = 'text'
    content = "欢迎订阅"

    return xmlText(toUser,fromUser,creatTime,msgType,content)


# 文本回复
def responseText(root):

    context = root.find('Content').text.lower()

    if context.find("介绍"):
        content = "全栈开发，bae部署，经济实惠。"

    toUser = root.find("FromUserName").text
    fromUser = root.find('ToUserName').text
    creatTime = str(int(time.time()))
    msgType = 'text'

    return xmlText(toUser,fromUser,creatTime,msgType,content)





@csrf_exempt
def index(request):
    # 与微信验证
    # 将timestamp，noce，token按字典排序
    if request.method == "GET":
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
        if not echostr:
            return HttpResponse("")

    # post接受到xml事件
    if request.method == "POST":

        tree = request.body
        if not tree:
            root = ET.fromstring(tree)
        else:
            return HttpResponse('xml不能解析')

        #事件
        if root.find('MsgType').text.lower() == "event":
            # 关注事件
            if root.find('Event').text.lower() == 'subscribe':
                return responseMsg(root)
           

        # 文本
        if root.find('MsgType').text.lower() == "text":
            return responseText(root)


        

    






    
    

