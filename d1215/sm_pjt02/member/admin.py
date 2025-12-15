from django.contrib import admin
# admin에 Member등록
from .models import Member

admin.site.register(Member)