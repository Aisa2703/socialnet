from django.shortcuts import render, HttpResponse


def Homepage(request):
    return HttpResponse("HelloWorld")


def Contacts(request):
    return HttpResponse("Наши контакты!")

def About_Us(request):
    return HttpResponse("Информация о нас!")

