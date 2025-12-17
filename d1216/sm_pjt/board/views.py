from django.shortcuts import render,redirect
from httpx import request
from board.models import Board
from member.models import Member
from django.db.models import F,Q


# 게시판 답글달기
def reply(request,bno):
    if request.method == 'GET':
        # 특정 게시글 가져오기
        qs = Board.objects.get(bno=bno)
        context = {'board':qs}
        return render(request,'board/reply.html',context)
    elif request.method == 'POST':
        # 답글 저장
        bgroup = request.POST.get('bgroup')
        bstep = int(request.POST.get('bstep'))
        bindent = int(request.POST.get('bindent'))  # 더해야하기 때문에 int로 변환
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent') 
        id = request.session.get('session_id')
        member = Member.objects.get(id=id)  # member 객체를 갖고옴
        bfile = request.FILES.get('bfile','') 
        
        # 1. 답글달기 : 우선 같은 그룹에 있는 게시글의 bstep 1씩 먼저 증가
        board_qd = Board.objects.filter(bgroup=bgroup, bstep__gt=bstep)  # bgroup 같고 bstep이 현재 bstep보다 큰것들 # filter : 여러개이기떄문
        board_qd.update(bstep=F('bstep')+1)  #bstep을 1씩 증가  # F함수 : 겁색된 그 컬럼에만 값을 적용 (F작성안하면 전체에 적용됨)
        
        # 2. 답글저장
        Board.objects.create(btitle=btitle,bcontent=bcontent,member=member,bgroup=bgroup,\
            bstep=bstep+1,bindent=bindent+1,bfile=bfile)
        
        
        context = {'flag':1}
        return render(request,'board/reply.html',context)

# 게시판 수정
def update(request,bno):
    if request.method == 'GET':
        # 특정 게시글 가져오기
        qs = Board.objects.get(bno=bno)
        context = {'board':qs}
        return render(request,'board/update.html',context)
    elif request.method == 'POST':
        id = request.session.get('session_id')
        member = Member.objects.get(id=id)
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        bfile = request.FILES.get('bfile')
        # 수정
        qs = Board.objects.get(bno=bno)
        qs.btitle = btitle
        qs.bcontent = bcontent
        if bfile: qs.bfile = bfile
        qs.save()
        return redirect(f'/board/view/{bno}/')
            
# 게시판 삭제
def delete(request,bno):
    # 특정 게시글 가져오기
    qs = Board.objects.get(bno=bno)
    qs.delete()
    context = {'flag':2}
    return redirect('/board/list/')


# 게시판 상세보기
def view(request,bno):
    # 특정 게시글 가져오기
    qs = Board.objects.filter(bno=bno)
    # 조회를 한 뒤 조회된 데이터들을 update,delete : F 객체 사용
    qs.update(bhit=F('bhit')+1)      # 조회수 1 증가
    context = {'board':qs[0]}
    return render(request,'board/view.html',context)

from django.core.paginator import Paginator

# 게시판 리스트
def list(request):
    # 게시글 모두 가져오기
    qs = Board.objects.all().order_by('-bgroup','bstep')    
    # 하단 넘버링
    paginator = Paginator(qs,10)   # 1페이지에 10개씩 자르기, 알아서 페이지 수 계산 
    #현재 페이지 넘김.
    page = int(request.GET.get('page',1 ))  # 현재 페이지 번호 가져오기, 기본값 1
    list_qs = paginator.get_page(page)   # 해당 페이지에 맞는 게시글들 가져오기
    
    # 페이지 범위 계산 (현재 페이지 기준 앞뒤 3개씩)
    start_page = max(1, page - 3)
    end_page = min(paginator.num_pages, page + 3)
    page_range = range(start_page, end_page + 1)
    
    context = {'list':list_qs,'page':page, 'page_range':page_range}
    return render(request,'board/list.html',context)

# 게시판 글쓰기
def write(request):
    if request.method == 'GET':
        return render(request,'board/write.html')
    elif request.method == 'POST':
        id = request.session.get('session_id')
        member_qs = Member.objects.get(id=id)
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        bfile = request.FILES.get('bfile','')
        # bgroup 값 입력
        qs = Board.objects.create(btitle=btitle,bcontent=bcontent,member=member_qs,bfile=bfile)
        qs.bgroup = qs.bno
        qs.save()
        context = {'flag':'1'}
        return render(request,'board/write.html',context)
        