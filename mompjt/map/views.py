from django.shortcuts import render


# ★ 지도 페이지
def map_view(request):
    return render(request, 'map/map.html')

