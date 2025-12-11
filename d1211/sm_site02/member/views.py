from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import Member


# 등록
def write(request):
    if request.method == 'GET':
        return render(request, 'member/write.html')
    elif request.method == 'POST':
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        hobby = request.POST.getlist('hobby')
        Member.objects.create(
            id=id,
            pw=pw,
            name=name,
            phone=phone,
            gender=gender,
            hobby=hobby
        )
        print("POST 확인 : ",id)
        return redirect('/')
    
    
# 전체 리스트
def list(request):
    qs = Member.objects.all().order_by('-mdate')
    context = {"list":qs}
    return render(request, 'member/list.html',context)

def login(request):
    return render(request, 'member/login.html')

def logout(request):
    return render(request, 'member/logout.html')
