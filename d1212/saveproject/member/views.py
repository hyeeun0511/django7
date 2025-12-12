from django.shortcuts import render,redirect

def login(request):
    if request.method == 'GET':
        # 쿠키 검색
        cooksave_id = request.COOKIES.get("cooksave_id","")   # 미리 적은 id를 읽어오는 명령어  -> ex) 아이디 : aaa  # "": 없을땐 빈공백 (""작성 안하면 None으로 뜸)
        context = {"cooksave_id":cooksave_id}                
        return render(request,'member/login.html',context)
    elif request.method == 'POST':
        id = request.POST.get("id")
        pw = request.POST.get("pw")
        login_keep = request.POST.get("login_keep")   # getlist(): 선택할게 여러개일 경우, 아이디저장 체크박스 1개라 get() 가능
        # 쿠키 읽기
        print("모든 쿠키 읽기 : ",request.COOKIES)
        # 쿠키저장
        response = redirect("/")  # 앱이름으로 찾아감  # ("index")도 가능 
        if login_keep:  
            print("아이디 저장이 체크가 되었습니다.")   # 프롬포트에 나타남
            ## 쿠키에 아이디를 저장시켜줌
            response.set_cookie("cooksave_id",id,max_age=60*60*24*30)  # 60*60*24*30 = 한달
            
        else:
            print("아이디 저장 체크가 되지 않았습니다.")
            response.delete_cookie("cooksave_id")
        print("post 입력된 데이터 : ",id,pw,login_keep)
        return response