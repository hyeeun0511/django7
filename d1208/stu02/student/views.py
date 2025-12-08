from django.shortcuts import render

# 학생리스트페이지
def list(request):
    return render(request,'list.html')


# 학생등록페이지
def write(request):
    return render(request,'write.html')
# 학생상세페이지
def view(request):
    return render(request,'view.html')
