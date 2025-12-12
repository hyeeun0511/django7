from django.shortcuts import render
from .models import Member

# 로그인 함수
def login(request):
    if request.method == 'GET':
        # 쿠키 읽어와서 context 저장해서 전송
        cook_id = request.COOKIES.get('cook_id','')  # 없으면 빈공백 전송
        context = {'cook_id':cook_id}
        return render(request,'member/login.html')  # 브라우저에 login.html화면을 보냄
    
    elif request.method == 'POST':  # post요청일때 로그인 버튼 클릭
        id = request.POST.get('id') # id : 로그인 입력값
        pw = request.POST.get('pw') # pw : 로그인 입력값
        login_keep = request.POST.get('login_keep') # login_keep : 로그인 유지 체크박스 값
        # id,pw 활용해서 로그인 체크
        qs = Member.objects.filter(id=id, pw=pw)  # id/pw 둘다 맞으면 qs에 데이터 들어감 / 틀리면 비어있음
                          # filter : 여러개 / 리스트 배열로 넘어옴
        
        if qs:  # 로그인 성공
            print("id/pw 일치 : ",id,pw)
            
            # session저장 (넣기만하면 바로 저장됨)
            request.session['session_id'] = id
            request.session['session_name'] = qs[0].name
            # 세션에 session_id,session_name 저장  ->  로그인 상태 유지
            
            context = {"state_code":"1"}  # html로 넘길 데이터
            response = render(request,'member/login.html',context)    # state_code=1  ->  로그인 성공 표시
            
            # 쿠키저장 ("로그인 유지" 체크할 경우)
            if login_keep:  # login_keep : 로그인 유지
                response.set_cookie("cook_id",id)    # cook_id에 id저장
            
            # 쿠키삭제  ("로그인 유지" 체크 안할 경우)
            else:
                response.delete_cookie("cook_id")   # cook_id 삭제
                
        else:   # 로그인 실패
            print("id/pw 불일치")
            context = {"state_code":"0"}
            response = render(request,'member/login.html',context)    # state_code=0  ->  로그인 실패 표시
        
        return  response
    
# 로그아웃
def logout(request):
    # 섹션 모두 삭제
    request.session.clear()
    context = {"state_code":"-1"}
    return render(request,'member/login.html',context)