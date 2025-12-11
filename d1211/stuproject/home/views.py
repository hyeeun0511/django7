from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request,'index.html')
    # return HttpResponse("메인")     # 메인 만들고 테스트  -> home > templates > index.html 생성
