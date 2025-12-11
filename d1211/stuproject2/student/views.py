from django.shortcuts import render


def write(request):
    return render(request, 'student/write.html')

def list(request):
    return render(request, 'student/list.html')

def view(request):
    return render(request, 'student/view.html')