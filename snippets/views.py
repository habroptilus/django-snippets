from django.http import HttpResponse
# from django.shortcuts import render
# Create your views here.


def top(request):
    return HttpResponse(b"Hello World")


def snippet_new(request):
    return HttpResponse("スニペットの登録")


def snippet_edit(request):
    return HttpResponse("スニペットの編集")


def snippet_detail(request):
    return HttpResponse("スニペットの詳細閲覧")
