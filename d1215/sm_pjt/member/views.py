from django.shortcuts import render
from .models import Member

# 로그인
def login(request):
    if request.method == 'GET':
        return render(request, 'member/login.html')
    elif request.method == 'POST':
        id = request.POST.get('id')   # 없을때 None
        pw = request.POST.get('pw')   # 없을때 None
        # try:
        #     id = request.POST['id']       # 없을때 에러
        # except:
        #     id = None
        
        qs = Member.objects.filter(id=id,pw=pw)  # filter : 없을때 에러나지 않음 => [] (빈공백)
        if qs:
            # 섹션추가
            request.session['session_id'] = id
            request.session['session_name'] = qs[0].name   # qs는 배열로 넘어옴 name:db(database에 있는 name이 넘어옴)
            context = {'flag':'1'}
        else:
            context = {'flag':'0','id':id,'pw':pw}
        # try:
        #     qs = Member.objects.get(id=id,pw=pw)     # get : 없을때 에러
        # except:
        #     qs = None    

        
        return render(request,'member/login.html',context)
    
    
# 로그아웃
def logout(request):
    request.session.clear()   # request에 있는 모든 session을 clear
    context = {'flag':'-1'}
    return render(request,'member/login.html',context)  # 로그아웃을 누를 시(def logout) -> 로그인 페이지(member/login.html)로 이동