from django.shortcuts import render,redirect
from customer.models import Board
from member.models import Member
from django.core.paginator import Paginator
from django.db.models import F,Q,Sum,Count    # 검색할때 필요


## 게시글 작성 (글쓰기 폼페이지 이동)
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
        qs.bgroup = qs.bno  # 방금 저장된 글의 bno를 bgroup에 넣기
        qs.save()
        return redirect('/customer/clist/')  # redirect : url로 보내줌



## 이전글. 다음글
def cview(request,bno):
    qs = Board.objects.get(bno=bno)
    
    # bgroup 역순정렬, bstep 순차정렬
    
    # 이전글---------------------------  lt : less than  /  lte : less than equal
    pre_qs = Board.objects.filter(Q(bgroup__lt=qs.bgroup)).order_by("-bgroup","bstep").first()
    # 답글달기가 포함 되어 있을때 쿼리문
    # pre_qs = Board.objects.filter(Q(bgroup__lt=qs[0].bgroup,bstep__lte=qs[0].bstep)|Q(bgroup=qs[0].bgroup,bstep__gt=qs[0].bstep)).order_by("-bgroup","bstep").first()
    print("이전글 : ",pre_qs)

    
    # 다음글---------------------------  gt : greater than  /  gte : greater than equal
    next_qs = Board.objects.filter(Q(bgroup__gt=qs.bgroup)).order_by("bgroup","-bstep").first() 
    # 답글달기가 포함 되어 있을때 쿼리문
    # next_qs = Board.objects.filter(Q(bgroup__gt=qs[0].bgroup,bstep__gte=qs[0].bstep)|Q(bgroup=qs[0].bgroup,bstep__lt=qs[0].bstep)).order_by("bgroup","-bstep").first()
    print("다음글 : ",next_qs)
    
    context = {'c':qs,'pre_c':pre_qs,'next_c':next_qs}
    return render(request,'customer/cview.html',context)


## 게시글 목록 검색
def clist(request):
    # 검색부분--------------------------------------------------------------
    category = request.GET.get('category','')  # 검색카테고리
    search = request.GET.get('search','')  # 검색어
    print("검색으로 넘어온 데이터:",category,search)
    # 검색부분--------------------------------------------------------------
    if not search:
        qs = Board.objects.all().order_by('-bgroup','bstep')
    else:
        if category == 'btitle':   # 제목검색
            qs = Board.objects.filter(btitle__contains=search)
        elif category == 'bcontent':   # 내용검색
            qs = Board.objects.filter(bcontent__contains=search)
        elif category == 'all':   # 통합검색
            qs = Board.objects.filter(Q(btitle__contains=search) | Q(bcontent__contains=search))

    
    ## 게시글 하단페이지 넘버링 ------------------------------------------------------
    # Pagenator는 꼭 요청페이지 번호가 있어야 함
    # 요청페이지번호 : int타입
    page = int(request.GET.get('page',1))  # 없으면 1번 페이지 호출  # 현재 요청하는 페이지
    paginator = Paginator(qs, 10)  # Show 10 items per page
    list_qs = paginator.get_page(page)
    ## 게시글 하단페이지 넘버링 ------------------------------------------------------
    
    context = {'list': list_qs,'page':page,'category':category,'search':search}  # 페이지 번호도 넘김
    return render(request,'customer/clist.html', context)



#------------------------------------
# [ 하단넘버링 ]
# 이전페이지 유므 : list.has_previous
# 이전페이지 번호 : list.previous_page_number
# 다음페이지 유므 : list.has_next
# 다음페이지 번호 : list.next_page_number
# 총페이지수 : list.paginator.num_pages
#------------------------------------