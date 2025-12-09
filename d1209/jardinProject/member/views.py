from django.shortcuts import render

def write(request):
    return render(request,'member/write.html')