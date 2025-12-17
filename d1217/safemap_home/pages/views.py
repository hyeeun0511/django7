from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.db.utils import OperationalError

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
