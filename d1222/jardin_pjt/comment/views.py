from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from comment.models import Comment
from member.models import Member
from customer.models import Board


def colist(request):
    # list타입으로 변경을 해서 Json타입으로 변경을 해야 함.
    # objects.filter(), objects.all() -> list타입
    return JsonResponse()

def codelete(request):
    cno = request.POST.get('cno')
    Comment.objects.get(cno=cno).delete()
    context = {'result':'성공'}
    return JsonResponse(context)

def cowrite(request):
    # list타입으로 변경을 해서 Json타입으로 변경을 해야 함.
    # objects.filter(), objects.all() -> list타입
    # 넘어온 데이터 확인
    id = request.session['session_id']
    member = Member.objects.get(id=id)
    bno = request.POST.get('bno')
    board = Board.objects.get(bno=bno)
    cpw = request.POST.get('cpw','')
    ccontent = request.POST.get('ccontent','')
    print('넘어온 데이터 : ',cpw,ccontent)

    # db저장부분 - cno : 자동생성(primary Key)
    qs = Comment.objects.create(cpw=cpw,ccontent=ccontent,member=member,board=board)
    l_qs = list(Comment.objects.filter(cno=qs.cno).values())
    print("l_qs 데이터 형태 : ",l_qs)
    context = {'result':'성공','co':l_qs}
    return JsonResponse(context)