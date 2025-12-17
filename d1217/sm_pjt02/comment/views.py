from django.shortcuts import render
from comment.models import Comment
from board.models import Board
from member.models import Member
from django.http import JsonResponse,HttpResponse # 전송할때 Json타입으로 변경해서 전송
from django.core import serializers  # Json타입으로 전달된 데이터를 파이썬데이터(set)로 변경
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime

# 하단댓글 부분 - 리턴타입이 Json형태로 변경해서 반환
def clist(request):
    # Json타입변경 - QuerySet List타입은 list타입으로 바로 변경
    qs = Comment.objects.filter(cno=1)
    list_qs = list(qs.values())  # QuerySet → 리스트 of dict
    context = {'result': 'success', 'list': list_qs}
    return JsonResponse(context)

    # # Json타입변경 - QuerySet List타입은 list타입으로 바로 변경
    # qs = Comment.objects.filter(cno=1)
    # l_qs = serializers.serialize('json',qs) #json타입으로 변환
    # print(l_qs)
    # context = {'result':'success','list':l_qs}
    # return JsonResponse(context)
    
    
    ##DateTimeField 타입, FileField 타입 -> 제대로 Json타입으로 변경이 안됨.
    # qs = Comment.objects.all()
    # l_qs = serializers.serialize('json',qs) #json타입으로 변환
    # # HttpResponse 데이터 자체를 리턴해줌.
    # return HttpResponse(l_qs,content_type='application/json')
    
    
