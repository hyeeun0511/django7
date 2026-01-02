from django.shortcuts import render,redirect
from customer.models import Board
from comment.models import Comment
from member.models import Member
from django.core.paginator import Paginator
from django.db.models import F,Q,Sum,Count

def cwrite(request):
    if request.method == 'GET':
        return render(request,'customer/cwrite.html')
    elif request.method == 'POST':
        id = request.session['session_id']
        member = Member.objects.get(id=id)
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        bfile = request.FILES.get('bfile')
        # db에 저장
        qs = Board.objects.create(member=member,btitle=btitle,bcontent=bcontent,bfile=bfile)
        qs.bgroup = qs.bno
        qs.save()
        return redirect('/customer/clist/')
        

# 고객센터 페이지 뷰 ----------------------------
def cview(request,bno):
    # 1개 게시글
    qs = Board.objects.get(bno=bno)
    # 하단댓글
    comment_qs = Comment.objects.all().order_by('-cno')

    # bgroup 역순정렬, bstep 순차정렬
    #이전글-----
    pre_qs = Board.objects.filter(bgroup__lt=qs.bgroup).order_by("-bgroup","bstep").first()
    # 답글달기가 포함 되어 있을때 쿼리문
    # pre_qs = Board.objects.filter(Q(bgroup__lt=qs[0].bgroup,bstep__lte=qs[0].bstep)|Q(bgroup=qs[0].bgroup,bstep__gt=qs[0].bstep)).order_by("-bgroup","bstep").first()
    print("이전글 : ",pre_qs)
    #다음글-----
    next_qs = Board.objects.filter(bgroup__gt=qs.bgroup).order_by('bgroup','-bstep').first()
    # 답글달기가 포함 되어 있을때 쿼리문
    # next_qs = Board.objects.filter(Q(bgroup__gt=qs[0].bgroup,bstep__gte=qs[0].bstep)|Q(bgroup=qs[0].bgroup,bstep__lt=qs[0].bstep)).order_by("bgroup","-bstep").first()
    print("다음글 : ",next_qs)

    context = {'c':qs,'pre_c':pre_qs,'next_c':next_qs,'comment_qs':comment_qs}
    return render(request,'customer/cview.html',context)

def clist(request):
    # 검색부분-------------------------------------------------
    category = request.GET.get('category','')
    search = request.GET.get('search','')
    print("검색으로 넘어온 데이터 : ",category,search)
    #--------------------------------------------------------
    if not search:
        qs = Board.objects.all().order_by('-bgroup','bstep')
    else:
        if category == 'btitle':
            qs = Board.objects.filter(btitle__contains=search)
        elif category == 'bcontent':
            qs = Board.objects.filter(bcontent__contains=search)
        elif category == 'all':
            qs = Board.objects.filter(Q(btitle__contains=search)|Q(bcontent__contains=search))
    
    # 하단페이지 넘버링-----------------------------------------
    # Pagenator는 꼭 요청페이지 번호가 있어야 함.
    # 요청페이지번호 : int타입
    page = int(request.GET.get('page',1)) # 없으면 1번 페이지 호출
    paginator = Paginator(qs,7)
    list_qs = paginator.get_page(page)
    # -------------------------------------------------------
    
    context = {'list':list_qs,'page':page,'category':category,'search':search}
    return render(request,'customer/clist.html',context)



# -----------------------------------------------
# [ 하단넘버링 ]
# * 이전페이지 유무 : {% if list.has_previous %}

