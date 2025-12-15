from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import Board
from member.models import Member
from django.db.models import F,Q

# 답변달기
def reply(request,bno):    # reply -> update와 폼이 같은
    if request.method == 'GET':
        qs = Board.objects.get(bno=bno)
        context = {"board":qs}
        return render(request,'board/reply.html',context)
    elif request.method == 'POST':
        bgroup = int(request.POST.get('bgroup'))     # 타입이 문자열 ->int로 변경
        bstep = int(request.POST.get('bstep'))       # 답글 순서
        bindent = int(request.POST.get('bindent'))   # 들여쓰기   ex) ㄴ답글입니다.
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        id = request.session['session_id']
        qs2 = Member.objects.get(id=id)   #(컬럼명(변수)=값)
        # 1. bgroup에서 부모보다 bstep 더 높은 값을 검색                     # bgroup이 같으면서 부모보다 bstep이 더 높은 값을 검색
        bstepup_qs = Board.objects.filter(bgroup=bgroup,bstep__gt=bstep)  # 현재 bgroup과 같은 bgroup을 찾고/ 현재의 bstep보다 큰것  
        # 2. 검색된 데이터에서 bstep을 뽑아서 1씩 증가
        bstepup_qs.update(bstep=F('bstep')+1)  
        
        
        # 답변달기 저장
        Board.objects.create(btitle=btitle,bcontent=bcontent,member=qs2,\
            bgroup=bgroup,bstep=bstep+1,bindent=bindent+1)
        return redirect('/board/list?flag=2')  # request->flag

# 게시글 수정
def update(request,bno):
    if request.method == 'GET':
        print("수정url : ",bno)
        # Board테이블에서 bno=1
        qs = Board.objects.get(bno=bno)
        context = {'board':qs}
        return render(request,'board/update.html',context) 
    elif request.method == 'POST':
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        id = request.session['session_id']
        # 수정저장이 완료되면  
        context ={'flag':1}   # -> 성공했다는 의미로 flag1을 보내줌
        # 수정내용 저장
        qs = Board.objects.get(bno=bno)
        qs.btitle = btitle
        qs.bcontent = bcontent
        qs.save()
        return redirect(f'/board/view/{bno}/')

# 게시글 삭제
def delete(request,bno):
    print("url : ",bno)
    # Board테이블에서 bno=1
    qs = Board.objects.get(bno=bno)
    qs.delete()
    return redirect('/board/list/') 

# 게시글 상세보기
def view(request,bno):         # urls.py에서 링크를 bno로 넘겼으므로 bno작성해주기
    print("url : ",bno)
    # Board테이블에서 bno=1
    qs = Board.objects.get(bno=bno)
    context = {'board':qs}
    return render(request,'board/view.html',context)    # ,context 꼭 작성하기

# 게시판 리스트
def list(request):
    qs = Board.objects.all().order_by('-bgroup','bstep')  # -bno : 역순정렬  # bgroup이 같으면 bstep으로
    flag = request.GET.get("flag",'')  # 없을땐 빈공백, 답변이 있다면 flag를 list에 넘기라는 의미
    print(qs)
    context = {'list':qs,'flag':flag}
    return render(request,'board/list.html',context)

# 글쓰기 화면 / 글쓰기 저장
def write(request):
    if request.method == 'GET':
        return render(request,'board/write.html')
    elif request.method == 'POST':
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        id = request.session['session_id']
        # member객체를 저장해야함 (id를 바로 저장할수 엇음)
        qs2 = Member.objects.get(id=id)
        qs = Board.objects.create(btitle=btitle,bcontent=bcontent,member=qs2)  # member객체를 저장해서 qs를 가져옴
        # bno번호를 bgroup에 다시 저장     (# 답변달기를 하려면 bgroup무조건 만들어야함)  # 답변 달때만 번호가 다르게 부여됨
        qs.bgroup = qs.bno    # bgroup 과 bno 가 같아짐  
        qs.save()
        context = {'flag':'1'}
        return render(request,'board/write.html',context)
        