from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from .models import Report
from .forms import ReportForm
from .services import classify_category, risk_score, one_line_summary

def map_view(request):
    return render(request, 'reports/map.html')

@login_required
def new_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            r: Report = form.save(commit=False)
            r.user = request.user
            category = classify_category(r.title + " " + r.content)
            risk = risk_score(category, r.title + " " + r.content)
            r.category = category
            r.risk = risk
            r.summary = one_line_summary(r.title, category, risk, r.content)
            r.save()
            messages.success(request, "제보 등록 완료! 지도에서 바로 확인 ㄱㄱ")
            return redirect('reports:detail', pk=r.pk)
    else:
        form = ReportForm()
    return render(request, 'reports/new.html', {'form': form})

@login_required
def my_reports(request):
    qs = Report.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'reports/my.html', {'reports': qs})

def detail(request, pk):
    r = get_object_or_404(Report, pk=pk)
    return render(request, 'reports/detail.html', {'r': r})

def api_list(request):
    days = int(request.GET.get('days', '7'))
    now = timezone.now()
    qs = Report.objects.filter(created_at__gte=now - timedelta(days=days)).order_by('-created_at')[:500]
    data = []
    for r in qs:
        data.append({
            'id': r.id,
            'title': r.title,
            'summary': r.summary,
            'category': r.category,
            'risk': r.risk,
            'lat': r.lat,
            'lng': r.lng,
            'happened_at': r.happened_at.isoformat(),
            'detail_url': f"/reports/{r.id}/",
        })
    return JsonResponse({'count': len(data), 'items': data})
