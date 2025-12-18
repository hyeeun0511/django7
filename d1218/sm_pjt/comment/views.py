from django.shortcuts import render
from comment.models import Comment
from board.models import Board
from member.models import Member
from django.http import JsonResponse



# 4. 하단댓글 수정  cupdate


# 3. 하단댓글 삭제   cdelete
def cdelete(request):
    if request.method == 'POST':
        cno = request.POST.get('cno')
        Comment.objects.get(cno=cno).delete()
        context = {'result':'성공'}
        return JsonResponse(context) # context를 json타입으로 변경해서 전송


# 2. 하단댓글 추가
def cwrite(request):
    if request.method == 'POST':
        id = request.session.get('session_id')
        member = Member.objects.get(id=id)
        bno = request.POST.get('bno')
        board = Board.objects.get(bno=bno)
        cpw = request.POST.get('cpw')
        ccontent = request.POST.get('ccontent')
        print(f"bno: {bno}, cpw:{cpw}, ccontent:{ccontent}")
    
        qs = Comment.objects.create(board=board,cpw=cpw,ccontent=ccontent,member=member)
        c_qs = list(Comment.objects.filter(cno=qs.cno).values())
        context = {'result': 'success', 'comment':c_qs[0]}
        return JsonResponse(context)


# 1. 하단댓글 리스트
def clist(request):
    bno = request.GET.get('bno')
    print("bno 확인 : ",bno)
    board = Board.objects.get(bno=bno)
    qs = Comment.objects.filter(board=board).order_by('-cno')
    list_qs = list(qs.values())
    context = {'result': 'success', 'list':list_qs}
    return JsonResponse(context)