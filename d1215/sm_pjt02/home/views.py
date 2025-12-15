from django.shortcuts import render

def index(request):
    return render(request, 'index.html')  
# home의 html -> index.html
# 사용자가 메인페이지에 들어왔을때 index.html 파일을 화면에 보여줌