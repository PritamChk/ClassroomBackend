from http.client import HTTPResponse
from django.shortcuts import render
from django.http import HttpResponse

def test(request):
    return HttpResponse("hello")
