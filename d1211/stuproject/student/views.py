from django.shortcuts import render,redirect
from django.urls import reverse  
from django.http import HttpResponse
from .models import Student
# 학생등록페이지
def write(request):
    # 1) GET 요청 : 화면만 보여줄 때
    if request.method == 'GET':
        # student/write.html 템플릿을 화면에 보여줌
        return render(request, 'student/write.html')
    # 2) POST 요청 : 폼에서 "등록" 버튼을 눌렀을 때
    elif request.method == 'POST':
        # 화면에서 넘어온 값 꺼내기
        # name="..." 과 같은 이름으로 넘어온다.
        name = request.POST.get('name')      # 이름
        age = request.POST.get('age')        # 나이
        grade = request.POST.get('grade')    # 학년
        gender = request.POST.get('gender')  # 성별
        # checkbox는 여러 개가 선택될 수 있으므로 getlist() 사용
        hobby = request.POST.getlist('hobby')  # ['게임', '독서'] 이런 식으로 리스트로 옴
        # txt =f'{sno},{name},{age},{grade},{gender},{hobby}'    # 확인용
        # return HttpResponse(f"post입력 : {txt}")
        # Student db 저장
        qs = Student(
            name=name,
            age=age,
            grade=grade,
            gender=gender,
            hobby=hobby)
        qs.save()
        print("POST 확인,저장 : ",name)
        return redirect(reverse('student:list'))
# 학생리스트페이지
def list(request):
    qs = Student.objects.all().order_by('-sno')
    context = {'list':qs}
    return render(request, 'student/list.html',context)
# 학생상세보기페이지
def view(request,sno):
    qs = Student.objects.get(sno=sno)
    context = {'stu':qs}
    return render(request, 'student/view.html',context)
# 학생삭제페이지
def delete(request,sno):
    qs = Student.objects.get(sno=sno)
    qs.delete()  # 삭제
    return redirect(reverse('student:list'))

# 학생수정페이지
def update(request,sno):
    # 1) GET 요청 : 화면만 보여줄 때
    if request.method == 'GET':
        qs = Student.objects.get(sno=sno)
        context = {"stu":qs}
        return render(request, 'student/update.html',context)
    elif request.method == 'POST':
        name = request.POST.get('name')      # 이름
        age = request.POST.get('age')        # 나이
        grade = request.POST.get('grade')    # 학년
        gender = request.POST.get('gender')  # 성별
        hobby = request.POST.getlist('hobby')  # ['게임', '독서'] 이런 식으로 리스트로 옴
        qs = Student.objects.get(sno=sno)
        qs.name = name
        qs.age = age
        qs.grade = grade
        qs.gender = gender
        qs.hobby = hobby
        qs.save()
        print("POST 확인,저장 : ",name)
        return redirect(reverse('student:list'))