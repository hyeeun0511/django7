from django.shortcuts import render,redirect,get_object_or_404   # redirect,get_object_or_404 추가   251223 혜은===========
from django.utils import timezone
from datetime import timedelta
from django.db.utils import OperationalError
# 혜은 =========================================
from .models import Board
from django.http import HttpResponseForbidden       # 251224 혜은===========게시물 삭제
# 혜은 =========================================
from django.http import JsonResponse, HttpResponseBadRequest
import requests
from functools import lru_cache
import time
from django.core.paginator import Paginator    # 251223 혜은===========


try:
    from reports.models import Report
except Exception:
    Report = None


def home(request):
    now = timezone.now()
    last7 = 0
    last30 = 0
    avg_risk_7 = 0

    if Report is not None:
        try:
            last7 = Report.objects.filter(created_at__gte=now - timedelta(days=7)).count()
            last30 = Report.objects.filter(created_at__gte=now - timedelta(days=30)).count()
            risks = list(Report.objects.filter(created_at__gte=now - timedelta(days=7)).values_list('risk', flat=True))
            avg_risk_7 = round(sum(risks) / len(risks), 2) if risks else 0
        except OperationalError:
            last7 = last30 = 0
            avg_risk_7 = 0

    return render(request, 'pages/home.html', {'last7': last7, 'last30': last30, 'avg_risk_7': avg_risk_7})

def about(request):
    return render(request, 'pages/about.html')

# --- KR Admin Proxy (Overpass) ---

# Simple in-process TTL cache
_cache_store = {}
_CACHE_TTL_SEC = 60 * 60  # 1 hour

def _cache_get(key):
    item = _cache_store.get(key)
    if not item:
        return None
    ts, value = item
    if time.time() - ts > _CACHE_TTL_SEC:
        _cache_store.pop(key, None)
        return None
    return value

def _cache_set(key, value):
    _cache_store[key] = (time.time(), value)

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

def _overpass(query):
    try:
        r = requests.post(OVERPASS_URL, data={"data": query}, timeout=25)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"elements": []}

def _list_sido():
    key = "sido:list"
    cached = _cache_get(key)
    if cached is not None:
        return cached
    q = (
        "[out:json][timeout:25];"
        "rel[boundary=administrative][admin_level=2][name=\"대한민국\"];"
        "map_to_area->.kr;"
        "rel(area.kr)[boundary=administrative][admin_level=4][name];"
        "out tags;"
    )
    j = _overpass(q)
    names = sorted({(e.get('tags') or {}).get('name') for e in j.get('elements', []) if (e.get('tags') or {}).get('name')})
    _cache_set(key, names)
    return names

def _list_sigungu(sido_name: str):
    key = f"sigungu:{sido_name}"
    cached = _cache_get(key)
    if cached is not None:
        return cached
    q = (
        "[out:json][timeout:25];"
        f"rel[boundary=administrative][admin_level=4][name=\"{sido_name}\"];"
        "map_to_area->.a;"
        "rel(area.a)[boundary=administrative][admin_level=6][name];"
        "out tags;"
    )
    j = _overpass(q)
    names = sorted({(e.get('tags') or {}).get('name') for e in j.get('elements', []) if (e.get('tags') or {}).get('name')})
    _cache_set(key, names)
    return names

def _list_dong(sido_name: str, sigungu_name: str):
    key = f"dong:{sido_name}:{sigungu_name}"
    cached = _cache_get(key)
    if cached is not None:
        return cached
    # Find area for the given sigungu within the sido, then list admin_level 8/9/10 names
    q = (
        "[out:json][timeout:25];"
        f"rel[boundary=administrative][admin_level=4][name=\"{sido_name}\"];"
        "map_to_area->.sido;"
        f"rel(area.sido)[boundary=administrative][admin_level=6][name=\"{sigungu_name}\"];"
        "map_to_area->.sgg;"
        "rel(area.sgg)[boundary=administrative][admin_level~\"8|9|10\"][name];"
        "out tags;"
    )
    j = _overpass(q)
    names = sorted({(e.get('tags') or {}).get('name') for e in j.get('elements', []) if (e.get('tags') or {}).get('name')})
    _cache_set(key, names)
    return names

def kr_admin(request):
    # Modes:
    #  - GET /pages/api/kr-admin/?level=sido -> [sido]
    #  - GET /pages/api/kr-admin/?sido=서울특별시 -> [sigungu]
    #  - GET /pages/api/kr-admin/?sido=서울특별시&sigungu=강남구 -> [dong]
    level = request.GET.get('level')
    sido = request.GET.get('sido')
    sigungu = request.GET.get('sigungu')

    if level == 'sido' or (not sido and not sigungu):
        return JsonResponse({"level": "sido", "items": _list_sido()})

    if sido and not sigungu:
        items = _list_sigungu(sido)
        return JsonResponse({"level": "sigungu", "sido": sido, "items": items})

    if sido and sigungu:
        items = _list_dong(sido, sigungu)
        return JsonResponse({"level": "dong", "sido": sido, "sigungu": sigungu, "items": items})

    return HttpResponseBadRequest("Invalid parameters")



# 혜은 [게시글 페이지 번호]=========================================
def board_list(request):
    board_qs = Board.objects.all().order_by('-id')  # 최신글 먼저

    paginator = Paginator(board_qs, 5)             # ✅ 한 페이지 5개
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # ✅ 전체 게시글 수
    total_count = board_qs.count()

    # ✅ 5개씩 묶음(1~5, 6~10 ...) 계산
    group_size = 5
    current = page_obj.number
    start_page = ((current - 1) // group_size) * group_size + 1
    end_page = min(start_page + group_size - 1, paginator.num_pages)
    page_range = range(start_page, end_page + 1)

    return render(request, 'board_list.html', {
        'page_obj': page_obj,
        'page_range': page_range,
        'start_page': start_page,
        'end_page': end_page,
        'total_count': total_count,
    })
# 혜은 [게시글 페이지 번호]=========================================

# 혜은 251223=[게시글작성]========================================
# @login_required  # 나중에 로그인 기능 추가 시 활성화
def board_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        # ✅ 게시글을 "한 번만" 저장 + author 포함
        Board.objects.create(
            title=title,
            content=content,
            author=request.user
        )

        return redirect('pages:board_list')

    return render(request, 'board_create.html')
# 혜은 251223=========================================


# 혜은 1223======게시글 상세페이지 뷰 ==========================
def board_detail(request, pk):
    board = get_object_or_404(Board, pk=pk)

    prev_post = Board.objects.filter(id__lt=board.id).order_by('-id').first()
    next_post = Board.objects.filter(id__gt=board.id).order_by('id').first()

    # ✅ (추가) 몇 페이지에서 왔는지 (예: /board/14/?from=2)
    from_page = request.GET.get('from', 1)

    # ✅ (기존 board_list 자리) 상세 하단에 보여줄 "게시글 목록"을 해당 페이지로 구성
    board_qs = Board.objects.all().order_by('-id')  # 목록과 동일한 정렬
    paginator = Paginator(board_qs, 5)              # ✅ board_list와 같은 개수(5개씩)
    board_list = paginator.get_page(from_page)      # ✅ from_page에 해당하는 페이지 객체

    return render(request, 'reports/board_detail.html', {
        'board': board,
        'prev_post': prev_post,
        'next_post': next_post,

        # ✅ 하단 목록(페이지 객체)
        'board_list': board_list,

        # ✅ 템플릿에서 링크/목록으로 이동 시 계속 유지용
        'from_page': from_page,
    })
# 혜은 1223======게시글 상세페이지 뷰 ==========================

# 혜은 251224===========게시물 삭제 ==========================
# @login_required  # 나중에 로그인 기능 추가 시 활성화
def board_delete(request, pk):
    board = get_object_or_404(Board, pk=pk)

    # # 🔒 작성자만 삭제 가능
    # if board.author != request.user:
    #     return HttpResponseForbidden("삭제 권한이 없습니다.")

    if request.method == 'POST':
        board.delete()
        return redirect('pages:board_list')

    # POST 외 접근 방지
    return redirect('pages:board_detail', pk=pk)
# 혜은 251224===========게시물 삭제 ==========================