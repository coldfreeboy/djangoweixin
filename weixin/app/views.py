from django.shortcuts import render,HttpResponse

# Create your views here.
def token(request):
    return HttpResponse('<h1>ok<h1>')