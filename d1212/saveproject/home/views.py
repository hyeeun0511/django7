from django.shortcuts import render

def index(request):
    # 쿠키 검색 - request(정보 저장소)
    # 쿠키 저장 - response
    
    # 쿠키 검색
    cook_info = request.COOKIES     # COOKIES -> 모든것을 다 찾을때
    print("쿠키모든정보 : ",cook_info)
    cook_id = request.COOKIES.get("cook_id","")  # cook_id - 있으때는 cook_id로 정보 갖고옴 / 없을땐 빈공백처리  # get -> 특정 하나를 찾을때
    print("cook_id 정보 : ",cook_id)
    
    response = render(request,'index.html')
    # # 쿠키저장 - response
    # cook_id = aaa   # key = value
    # 유지시간 없으면, 브라우저 종료시 사라짐, 시간을 설정하면 시간동안 유지
    # 쿠키정보가 없을때만 쿠키 저장
    # if not cook_id :   # cook_id가 not이면
    #     response.set_cookie("smsite_connect","ok")  # cook_id라는 key에 aaa라는 아이디를 넣어줌 
    #     response.set_cookie("ip","127.0.0.1:8000",max_age=60*60*24) # 60초*60분*24시간*365일    # 60 -> 60초  # 60*60 -> 60분 

        
    return response