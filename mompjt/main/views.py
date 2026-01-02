# ═══════════════════════════════════════════════════════════════════════
# main/views.py
# 맘스로그 프로젝트 - 메인 페이지 및 통합 검색 뷰
# ═══════════════════════════════════════════════════════════════════════
# 작성일: 2025-12-29
# 기능:
#   1. index: 메인 페이지 렌더링 (배너, 인기글, 로그인 박스)
#   2. search: 통합 검색 (공지사항, 자유게시판, 벼룩시장 전체 검색)
# ═══════════════════════════════════════════════════════════════════════

import json
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from itertools import chain
from operator import attrgetter
# 게시판 모델 import (Notice, FreePost, FleaItem)
from board.models import Notice, FreePost, FleaItem
from .models import GrowthRecord
from .forms import GrowthRecordForm

# ───────────────────────────────────────────────────────────────────────
# 메인 페이지
# ───────────────────────────────────────────────────────────────────────
def index(request):
    """
    맘스로그 메인 페이지
    - 배너 슬라이더 (베이비페어, 이유식, 실내놀이 등)
    - 실시간 인기글 표시
    - 로그인/로그아웃 박스
    """
    return render(request, 'main/index.html')


# ───────────────────────────────────────────────────────────────────────
# 성장 기록 그래프 (Chart.js)
# 25-12-29 슬기 수정: 키/몸무게 기록 + 시각화
# ───────────────────────────────────────────────────────────────────────
@login_required(login_url='accounts:login')
def growth_chart(request):
    form = GrowthRecordForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        record = form.save(commit=False)
        record.user = request.user
        record.save()
        return redirect('main:growth_chart')

    records = GrowthRecord.objects.filter(user=request.user).order_by('record_date')

    labels = [rec.record_date.strftime('%Y-%m-%d') for rec in records]
    heights = [float(rec.height_cm) for rec in records]
    weights = [float(rec.weight_kg) for rec in records]

    context = {
        'form': form,
        'records': records,
        'labels_json': json.dumps(labels, ensure_ascii=False),
        'heights_json': json.dumps(heights),
        'weights_json': json.dumps(weights),
    }
    return render(request, 'main/growth_chart.html', context)

# ───────────────────────────────────────────────────────────────────────
# 통합 검색 (공지사항 + 자유게시판 + 벼룩시장)
# 25-12-29 슬기 수정: 공지사항 검색 추가
# ───────────────────────────────────────────────────────────────────────
def search(request):
    """
    전체 게시판 통합 검색
    - 공지사항: 제목, 내용 검색
    - 자유게시판: 제목, 내용 검색
    - 벼룩시장: 제목, 설명 검색
    - 결과는 최신순으로 정렬하여 반환
    """
    query = request.GET.get('q', '')
    posts = []

    if query:
        # 1. 공지사항 검색 (제목, 내용)
        notice_results = Notice.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        # 꼬리표 달기 (템플릿에서 게시판 구분용)
        for post in notice_results:
            post.board_type = 'notice'

        # 2. 자유게시판 검색 (제목, 내용)
        free_results = FreePost.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        for post in free_results:
            post.board_type = 'free'

        # 3. 벼룩시장 검색 (제목, 설명)
        flea_results = FleaItem.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        for post in flea_results:
            post.board_type = 'flea'

        # 4. 결과 합치기
        posts = list(chain(notice_results, free_results, flea_results))

        # 5. 최신순 정렬 (created_at 기준)
        posts.sort(key=attrgetter('created_at'), reverse=True)

    context = {
        'posts': posts,
        'q': query,
    }
    return render(request, 'main/search_result.html', context)