from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id','title','category','risk','happened_at','created_at','user')
    search_fields = ('title','content')
    list_filter = ('category','risk')
