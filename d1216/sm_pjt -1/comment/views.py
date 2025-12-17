from django.shortcuts import render
from comment.models import Comment
from board.models import Board
from member.models import Member
from django.http import JsonResponse,HttpResponse # 전송할때 Json타입으로 변경해서 전송
from django.core import serializers  # Json타입으로 전달된 데이터를 파이썬데이터(set)로 변경
from django.core.serializers.json import DjangoJSONEncoder

# 하단댓글 부분
def list(request):
    # DateTimeField 타입, FileField 타입 -> 제대로 Json타입으로 변경이 안됨.
    qs = Board.objects.all()
    l_qs = serializers.serialize('json',qs) #json타입으로 변환
    # HttpResponse 데이터 자체를 리턴해줌.
    return HttpResponse(l_qs,content_type='application/json')
    
