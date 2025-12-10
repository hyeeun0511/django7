from django.shortcuts import render,redirect
from django.urls import reverse
#student에 있는 models를 사용해야해서
from .models import Student

# 학생등록함수
def write(request):
    if request.method == 'GET':
        return render(request,'student/write.html')
    elif request.method == 'POST':
        # form폼에서 넘어온 데이터 처리
        name = request.POST.get("name")
        age = request.POST.get("age")
        grade = request.POST.get("grade")
        gender = request.POST.get("gender")
        hobby = request.POST.getlist("hobby")
        # hobbys = ','.join(hobby)   # 리스트타입을 문자열타입으로 변환방법 (변환하지않으면 에러날수있음)
        # 리스트타입을 문자열항목에 저장하면 자동으로 형변환됨.
        Student(name=name,age=age,grade=grade,gender=gender,hobby=hobby).save()
        # Student.objects.create(name=name,age=age,grade=grade,gender=gender)      : 저장하는 다른 방법
        print("이름 : ",name)       # write.html에 있는것 갖고오기
        print("취미 : ",hobby)       # write.html에 있는것 갖고오기
        return redirect(reverse('student:list'))
        # return render(request,'student/write.html') 
        # redirect : 페이지 링크를 /student/list/ 로 넘겨주겠다는 의미
        

# 학생리스트함수
def list(request):
    # db명령어 - select,insert,update,delete
    qs = Student.objects.all().order_by('-sno','name')  # Student에 있는 objects 모든것을 가져온다  # order_by('age','-name') :나이가 같으면 같은것끼리 이름역순
    context = {"list":qs}  # {"name":"홍길자","student":qs}라는 형태로 qs를 넘김   # list : 변수명   => qs를 lsit에 넣으라는 의미  
    # 변수가 여러개라 context형태로 보내는것 선호
    # 위에 데이터를 request로 보내줌
    return render(request,'student/list.html',context)   # 함수로 와서 list페이지로 데이터 넘기기  # 함수 빠져나오면 모든 변수 사라짐


# 학생상세보기함수
def view(request,sno):   # 앞쪽(urls.py)에 2개받아서 여기도 두개받기  
    print("넘어온 데이터 sno : ",sno)
    qs = Student.objects.get(sno=sno)    # sno=1 1번 갖고오라는 뜻
    context = {"student":qs}  # student 변수이름
    return render(request,'student/view.html',context)   # 함수로 와서 list페이지로 데이터 넘기기



# 학생리스트함수
def delete(request):
    return render(request,'student/list.html')   # 함수로 와서 list페이지로 데이터 넘기기
