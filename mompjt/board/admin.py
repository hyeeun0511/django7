# -*- coding: utf-8 -*-
# ══════════════════════════════════════════════════════════════════════
# board/admin.py
# 맘스로그 프로젝트 - Django Admin 커스터마이징
# ══════════════════════════════════════════════════════════════════════
# 작성일: 2025-12-29
# Admin 클래스:
#   1. NoticeAdmin: 공지사항 관리
#   2. FreePostAdmin: 자유게시판 관리
#   3. FleaItemAdmin: 벼룩시장 관리 (25-12-29 수정 - 찜 개수, 거래 상태 표시)
#   4. FleaCommentAdmin: 벼룩시장 댓글 관리 (25-12-29 추가 - 초 단위 시간 표시)
#   5. NotificationAdmin: 알림 관리 (25-12-29 추가)
# ══════════════════════════════════════════════════════════════════════

from django.contrib import admin
from .models import Notice, FleaItem, FleaComment, Notification

class NoticeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'view_count')
    search_fields = ('title',)

admin.site.register(Notice, NoticeAdmin)

# 25-12-29 슬기 수정: 찜하기 기능, 찜 수 표시, 거래 상태 추가
@admin.register(FleaItem)
class FleaItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price_display', 'status', 'like_count', 'author', 'created_at')
    list_display_links = ('title',)
    list_filter = ('created_at', 'author', 'status')
    search_fields = ('title', 'description', 'author__username')
    readonly_fields = ('created_at', 'updated_at', 'author')
    
    fieldsets = (
        ('상품 정보', {
            'fields': ('title', 'price', 'description', 'image', 'status')
        }),
        ('기타 정보', {
            'fields': ('author', 'liked_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # 신규 작성 시 author 자동 설정
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    def price_display(self, obj):
        return f"{obj.price:,.0f}원"
    price_display.short_description = '가격'

    def like_count(self, obj):
        return obj.liked_by.count()
    like_count.short_description = '찜 수'


# 25-12-29 슬기 수정: 댓글 관리 (비밀글, 작성자, 작성일시 초단위 표시)
@admin.register(FleaComment)
class FleaCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'nickname', 'flea_item', 'is_secret', 'author', 'created_at_display')
    list_filter = ('is_secret', 'created_at')
    search_fields = ('title', 'content', 'nickname', 'author__username', 'flea_item__title')
    readonly_fields = ('created_at', 'updated_at', 'author', 'flea_item')
    
    def created_at_display(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M:%S')
    created_at_display.short_description = '작성일시'


# 25-12-29 슬기 수정: 알림 관리
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'actor', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('message', 'user__username', 'actor__username')
    readonly_fields = ('created_at', 'user', 'actor', 'flea_item', 'flea_comment')
