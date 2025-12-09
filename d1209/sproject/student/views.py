from django.shortcuts import render

def write(request):
    return render(request, 'student/write.html')
