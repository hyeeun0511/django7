from django.shortcuts import render,redirect
from django.http import HttpResponse
import requests
from django.conf import settings
import json

#---------------------------------------------------------------------카카오페이
# 제품상세페이지
def detail(request):
    return render(request, 'product/detail.html')

KAKAO_API_KEY = 'DEV225DD40545C02D3D0A4D0B6979377D53B0057'
KAKAOPAY_URL = 'https://open-api.kakaopay.com/online/v1/payment/ready'


# 카카오페이 준비 화면
def prepare_payment(request):
    # 상품명,판매가,수량 정보를 가져옴
    # - 상품명 : 쟈뎅 오리지널 콜롬비아 페레이라 원두커피백 15p
    # - 판매가 : 4,330원
    # - 수량 : 1개

    headers = {
        'Authorization':f'SECRET_KEY {KAKAO_API_KEY}',
        'Content-Type':'application/json',
    }

    # 결제정보
    data = {
        "cid": "TC0ONETIME",                     # 가맹점 코드 - 테스트 버전
        "partner_order_id": "partner_order_id",  # 가맹점 주문번호
        "partner_user_id": "partner_user_id",    # 가맹점 회원 id
        "item_name": "자뎅 원두커피백",            # 상품명
        "quantity": "1",                         # 상품 수량
        "total_amount": "4330",                  # 상품 총액
        "vat_amount": "433",                     # 부가세 금액
        "tax_free_amount": "0",                  # 비과세 금액
        "approval_url": "http://127.0.0.1:8000/product/approve",  # 결제 성공시 redirect url  # http://
        "fail_url": "http://127.0.0.1:8000/product/fail",         # 결제 실패시 redirect url
        "cancel_url": "http://127.0.0.1:8000/product/cancel"      # 결제 취소시 redirect url
    }

    # requests -> url에 있는 데이터 전송,응답
    # requests,response -> 브라우저에서 페이지를 열때 전달되는 객체
    response = requests.post(KAKAOPAY_URL, headers=headers, data=json.dumps(data,ensure_ascii=False))
    # data는 json형태로 변환해서 (data변수에 덮어써서)전달   # ensure_ascii=False : 한글깨짐 방지
    # 리턴받은 정보 - json으로 변환
    # 5개 리턴 : 결제 고유 번호, 앱일때, 모바일일때, pc일때 결제창 url정보 등
    result = response.json()
    print("리턴받은 결과 : ",result)
    # 섹션저장 - 결제 고유 번호

    request.session['tid'] = result['tid']  # tid : 결제고유번호
    request.session['order_id'] = data['partner_order_id']

    # 결제창을 넘겨줌
    print("결제창 화면: ",result['next_redirect_pc_url'])  # qr코드 or pc결제창 url

    if response.status_code == 200:  # 성공일때
        return redirect(result['next_redirect_pc_url'])
    else:
        return redirect('/product/fail/')  # 실패페이지로 이동

# 카카오페이 결제승인창
def approve(request):
    # 리턴받은 값
    pg_token = request.GET.get('pg_token')  # 카카오에서 보내주는 토큰
    tid = request.session.get('tid')        # 세션에 저장된 결제고유번호
    order_id = request.session.get('order_id')  # 세션에 저장된 주문번호
    print("리턴받은 값 : ",pg_token, tid, order_id)
    
    if not pg_token or not tid:  # 토큰이 없으면 실패페이지로 이동
        return redirect('/product/fail/')
    
    url='https://open-api.kakaopay.com/online/v1/payment/approve'  # 결제승인 url # 온라인 카톡으로 받는것 : https://
    headers = {
        'Authorization':f'SECRET_KEY {KAKAO_API_KEY}',
        'Content-Type':'application/json',
    }    
    
    data = {
        "cid": "TC0ONETIME",
		"tid": tid,
		"partner_order_id": order_id,
		"partner_user_id": "partner_user_id",
		"pg_token": pg_token
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data,ensure_ascii=False))
    print("리턴받은 결과 : ",response)
    result = response.json()  # 결제 정보 넘어옴
    print("결제 날짜 : ",result.get('created_at'))
    # print("결제 날짜 : ",result['created_at'])  # 키가 없으면 에러발생
    
    if result.get('aid'):  # aid : 결제 승인 번호
        # db에 저장 - 결제정보 저장
        # Payment.objects.create(           )
        
        print("결제 성공!!!")
        return redirect('/product/success/')
    
    return redirect('/product/fail/')


# 카카오페이 성공
def success(request):
    return HttpResponse("카카오페이 성공화면으로 변경")
# 카카오페이 실패
def fail(request):
    return HttpResponse("카카오페이 실패화면으로 변경")
# 카카오페이 취소
def cancel(request):
    return HttpResponse("카카오페이 취소화면으로 변경")