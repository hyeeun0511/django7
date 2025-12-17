from django.shortcuts import render,redirect
from board.models import Board
from member.models import Member
from django.db.models import F,Q

# 게시판 수정
def update(request,bno):
    if request.method == 'GET':
        # 게시글 가져오기
        qs = Board.objects.get(bno=bno)
        context = {'board':qs}
        return render(request,'board/update.html',context)

# 게시판 삭제
def delete(request,bno):
    # 게시글 가져오기
    qs = Board.objects.get(bno=bno)
    qs.delete()
    context = {'flag':2}
    return redirect("/board/list/")

# 게시판 상세보기
def view(request,bno):
    # 게시글 가져오기
    qs = Board.objects.filter(bno=bno)
    # 조회수 1증가
    # 조회를 한후 조회된 데이터들을 update,delete : F
    qs.update(bhit = F('bhit') + 1 )
    context = {'board':qs[0]}
    return render(request,'board/view.html',context)

from django.core.paginator import Paginator

# 게시판 리스트
def list(request):
    # 게시글 모두 가져오기
    qs = Board.objects.all().order_by('-bgroup','bstep')
    # 하단 넘버링 (qs,10) -> 1페이지 10개씩
    paginator = Paginator(qs,10)  # 101 -> 11
    # 현재페이지 넘김.
    page = int(request.GET.get('page',1))
    list_qs = paginator.get_page(page) # 1page -> 게시글 10개를 전달
    
    context = {'list':list_qs,'page':page}
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
        # bgroup 값을 입력
        qs = Board.objects.create(btitle=btitle,bcontent=bcontent,member=member_qs,bfile=bfile)
        qs.bgroup = qs.bno
        qs.save()
        context = {'flag':'1'}
        return render(request,'board/write.html',context)
        