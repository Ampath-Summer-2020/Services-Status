from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the status' services index.")


# def user_mail_link(request):
#     email = request.POST['field_id']
#     pass