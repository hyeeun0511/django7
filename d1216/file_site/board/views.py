from django.shortcuts import render,redirect
from board.models import Board
import datetime

# 게시글 작성
def write(request):
    if request.method == 'GET':
        return render(request, 'board/write.html')
    elif request.method == 'POST':
        btitle = request.POST.get('btitle')
        bfile = request.FILES.get('bfile')  # file타입이기에 FILES로 읽어야 함
        # 이름을 변경해서 저장하기도 함
        # bfile = f'{datetime.datetime.now().microsecond}_{bfile}'
        print('post btitle 정보 : ',btitle)
        print('post bfile 정보 : ',bfile)
        print("날짜: ",datetime.datetime.now())
        print("날짜: ",datetime.datetime.now().microsecond)  # 정밀한 시간측정
        
        # 파일저장
        qs = Board(btitle=btitle,bfile=bfile)
        qs.save()
        
        return render(request,'board/write.html')