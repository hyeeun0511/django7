from django.shortcuts import render

def write(request):
    return render(request, 'event/write.html')
