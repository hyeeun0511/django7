from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import chartData

def index(request):
    return render(request, 'main.html')

def chart(request):
    return render(request, 'chart1.html')

def chart2(request):
    return render(request, 'chart2.html')

# @csrf_exempt # CSRF 토큰 예외 처리 # 단순데이터 처리
def chart_json(request): 
    context = {'dd_data':[10, 5, 9, 8, 3, 6],'ll_data':['홍길동','유관순','이순신','강감찬','김구','김유신']} 
    return JsonResponse(context)

# @csrf_exempt # CSRF 토큰 예외 처리 # db데이터 처리
def chart_json2(request):
    qs = chartData.objects.all().order_by('cyear')
    # qs = chartData.objects.all()

    return JsonResponse({
        'll2_data': list(qs.values_list('cyear', flat=True)),
        'dd2_data': list(qs.values_list('cdata', flat=True)),
    })



