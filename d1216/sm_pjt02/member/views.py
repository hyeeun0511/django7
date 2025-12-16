from django.shortcuts import render
from .models import Member 

# 로그인
def login(request):
    if request.method == 'GET':
        # 처음 로그인 페이지 접속
        context = {'error': -1}  # 로그인 시도 안함
        return render(request, 'member/login.html', context)
    
    elif request.method == 'POST':
        # 로그인 버튼 눌렀을때
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        
        # DB에서 일치하는 회원 찾기
        qs = Member.objects.filter(id=id,pw=pw)
        
        if qs.exists():
            context = {'error': 1}  # 로그인 성공
        else:
            context = {'error': 0}  # 로그인 실패
            
        return render(request, 'member/login.html', context)
    
# 회원 리스트
def list(request):
    # DB에서 모든 회원 가져오기 (-mdate : 최신순)
    qs = Member.objects.all().order_by('-mdate')
    context = {'list': qs}  # 로그인 시도 안함
    return render(request, 'member/list.html', context)

# 회원 등록
def write(request):
    if request.method == 'GET':
        # 회원 등록페이지
        return render(request, 'member/write.html')
    
    elif request.method == 'POST':
        # 회원 등록버튼 눌렀을때
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        hobby_list = request.POST.getlist('hobby')
        hobby_str = ','.join(hobby_list)
        
        # DB에 회원정보 저장
        