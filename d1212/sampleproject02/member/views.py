from django.shortcuts import render
# from .models import Member


# 로그인 부분
def login(request):
    if request.method == 'GET':
        # 쿠키 있으면 cook_id 전송 / # 없으면 빈공백 전송
        cook_id = request.COOKIES.get('cook_id','')  
        context = {'cook_id':cook_id}
        return render(request,'member/login.html')
    elif request.method == 'POST':    
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        login_keep = request.POST.get('login_keep')
    
        
# 로그아웃 부분
def logout(request):
    return render(request,'member/login.html')