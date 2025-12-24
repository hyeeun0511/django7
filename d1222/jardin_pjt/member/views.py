from django.shortcuts import render,redirect
from django.http import JsonResponse
from member.models import Member

# 로그아웃
def logout(request):
    request.session.clear()  # 세션 데이터 모두 삭제
    
    return redirect('/')

# 로그인
def login(request):
    if request.method == 'GET':
        return render(request, 'member/login.html')
    elif request.method == 'POST':
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        print("넘어온 데이터 : ", id, pw)

        # id, pw DB에서 확인
        qs = Member.objects.filter(id=id, pw=pw)
        if qs:
            result = 1
            request.session['session_id'] = id  # 세션에 아이디 저장
            request.session['session_name'] = qs[0].name  # 세션에 이름 저장
        else: result = 0
        context = {'result': result}
        return render(request, 'member/login.html',context)

# 회원가입
def step03(request):
    return render(request, 'member/step03.html')

# json 리턴 : 아이디 중복체크
def idCheck(request):
    #db에서 확인
    id = request.GET.get('id','')
    qs = Member.objects.filter(id=id)
    if not qs:
        result = '사용가능'
    else: result = '사용불가'

    #-------------------

    context = {'result' : '사용가능'}
    return JsonResponse(context)