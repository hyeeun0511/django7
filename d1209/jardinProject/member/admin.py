from django.contrib import admin
# member 앱에서 models 파일안에 Member클래스 가져옴
from member.models import Member

admin.site.register(Member)  # admin사이트 밑에 등록해줌
