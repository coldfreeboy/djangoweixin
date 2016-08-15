#!coding:utf-8
from django.shortcuts import render,HttpResponse
import hashlib

# Create your views here.
def token(request):
    # 与微信验证
    # 将timestamp，noce，token按字典排序
    timestamp = request.GET.get('timestamp')
    nonce     = request.GET.get('nonce')
    taken     = "dangweiwu"
    signature = request.GET.get('signature')
    
    # 排序后进行sha1加密
    l = sorted([timestamp,nonce,taken])
    tmpstr = "".join(l)

    tmpstr = hashlib.sha1(tmpstr).hexdigest()
    
    # 验证成功返回echostr
    if signature == tmpstr:
        response = request.GET.get('echostr')

    return HttpResponse(response)