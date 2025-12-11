from django.shortcuts import render
from django.http import HttpResponse

# 메인페이지 호출
def index(request):
    return render(request, "index.html")