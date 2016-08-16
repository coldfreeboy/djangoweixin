#!coding:utf-8
from django.shortcuts import render,HttpResponse
import hashlib
import xml.etree.cElementTree as ET
import time

# Create your views here.
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
        
        # 验证成功返回echostr
        # if signature == tmpstr:
        #     if echostr:
        #         # 第一次验证会有echostr
        #         return HttpResponse(response)
        #     else:
        #         return HttpResponse(responseMsg(request),content_type="application/xml")

        if signature == tmpstr and echostr:
            return HttpResponse(echostr)

    if request.method == "POST":
        xmlstr = vresponseMsg(request)
        return HttpResponse(xmlstr,content_type="application/xml")    

        

    

def responseMsg(request):
    tree = request.body
    root = ET.fromstring(country_string)

    # '''
    # <xml>
    # <ToUserName><![CDATA[toUser]]></ToUserName>
    # <FromUserName><![CDATA[FromUser]]></FromUserName>
    # <CreateTime>123456789</CreateTime>
    # <MsgType><![CDATA[event]]></MsgType>
    # <Event><![CDATA[subscribe]]></Event>
    # </xml>
    # '''

    if root.find('MsgType').text.lower() == "event":
        if root.find('Event').text.lower() == 'subscribe':
            toUser = root.find("FromUserName").text
            fromUser = root.find('ToUserName').text
            creatTime = int(time.time())
            msgType = 'text'
            content = "欢迎订阅"
            template = """<xml>

            <ToUserName><![CDATA[%s]]></ToUserName>

            <FromUserName><![CDATA[%s]]></FromUserName>

            <CreateTime>%s</CreateTime>

            <MsgType><![CDATA[text]]></MsgType>

            <Content><![CDATA[%s]]></Content>

            </xml>"""%(toUser,fromUser,creatTime,content)
            return template




    
    

