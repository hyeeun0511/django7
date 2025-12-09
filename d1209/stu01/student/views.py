from django.shortcuts import render

# write 함수생성
def write(request):
    return render(request, 'write.html')
