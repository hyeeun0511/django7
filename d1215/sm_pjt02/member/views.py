from django.shortcuts import render,redirect
from .models import Member


# 로그인   -> member/templates/member/login.html
def login(request):
    if request.method == 'GET':
        context = {"error" : -1}
        return render(request, 'member/login.html', context)   # context : 변수이름  # GET으로 들어오면 -> 로그인 화면 보여줌
    
    elif request.method == 'POST':
        id = request.POST.get("id")
        pw = request.POST.get("pw")
        
        qs = Member.objects.filter(id=id,pw=pw)   # Member 선언 해줘야함  # id와 pw가 일치한다면
        
        if qs.exists():
            context = {'error': 1}  # 성공
        else:
            context = {'error': 0}  # 실패
            
        return render(request, 'member/login.html',context)
    
# 회원 리스트   -> member/templates/member/list.html 
def list(request):
    qs = Member.objects.all().order_by('-mdate')
    context = {'list':qs}
    return render(request, 'member/list.html',context)  # context -> qs와 list를 모두 연결시켜줌 -> ,context 필수로 넣어야함 

# 회원 등록    -> member/templates/member/write.html
def write(request):
    if request.method == 'GET':
        return render(request, 'member/write.html')  # write()는 템플릿에 넘겨줄 데이터 X / 즉, 화면만 출력 -> context 필요 X
    
    # 회원가입 / 글작성 POST폼 처리 형태
    elif request.method == 'POST':
        id = request.POST.get("id")
        pw = request.POST.get("pw")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        gender = request.POST.get("gender")
        hobby_list = request.POST.getlist("hobby")
        hobby_str = ",".join(hobby_str)
        
        Member.objects.create(
            id=id,
            pw=pw,
            name=name,
            phone=phone,
            gender=gender,
            hobby=hobby_str
        )
        
        return redirect('/')  # 메인으로