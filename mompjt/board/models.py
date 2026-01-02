# ═══════════════════════════════════════════════════════════════════════
# board/models.py
# 맘스로그 프로젝트 - 게시판 데이터 모델
# ═══════════════════════════════════════════════════════════════════════
# 작성일: 2025-12-29
# 모델:
#   1. Notice: 공지사항 (제목, 내용, 조회수)
#   2. FreePost: 자유게시판 (제목, 내용, 작성자, 조회수)
#   3. FleaItem: 벼룩시장 (제목, 설명, 가격, 이미지, 작성자, 찜 기능)
#   4. FleaComment: 벼룩시장 댓글 (25-12-29 추가 - 닉네임, 제목, 비밀글, 비밀번호)
# ═══════════════════════════════════════════════════════════════════════

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Notice(models.Model):
    title = models.CharField("제목", max_length=100)
    content = models.TextField("내용")
    created_at = models.DateTimeField("작성일", auto_now_add=True)
    view_count = models.IntegerField("조회수", default=0)

    class Meta:
        verbose_name = '공지사항'
        verbose_name_plural = '공지사항'

    def __str__(self):
        return self.title
    
    # 자유게시판
class FreePost(models.Model):
    title = models.CharField(max_length=200, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    
    # ▼▼▼ 여기 수정 (User -> settings.AUTH_USER_MODEL) ▼▼▼
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="작성자")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    views = models.IntegerField(default=0, verbose_name="조회수")

    class Meta:
        verbose_name = '자유게시판'
        verbose_name_plural = '자유게시판'

    def __str__(self):
        return self.title


class FleaItem(models.Model):
    # 25-12-29 슬기 수정: 거래 상태 필드 추가
    STATUS_CHOICES = [
        ('selling', '판매중'),
        ('reserved', '예약중'),
        ('sold', '판매완료'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="제목")
    description = models.TextField(verbose_name="내용")
    price = models.IntegerField(verbose_name="가격(원)")
    image = models.ImageField(upload_to='flea/', null=True, blank=True, verbose_name="이미지")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="작성자")
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_flea_items', blank=True, verbose_name="찜한 사용자")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='selling', verbose_name="거래 상태")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")

    class Meta:
        verbose_name = '벼룩시장'
        verbose_name_plural = '벼룩시장'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# 25-12-29 슬기 수정: 벼룩시장 댓글 모델 추가 (닉네임, 제목, 내용, 비밀글, 비밀번호)
class FleaComment(models.Model):
    flea_item = models.ForeignKey(FleaItem, on_delete=models.CASCADE, related_name='comments', verbose_name='상품')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='작성자')
    nickname = models.CharField(max_length=50, verbose_name='닉네임')
    title = models.CharField(max_length=200, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    is_secret = models.BooleanField(default=False, verbose_name='비밀글')
    password = models.CharField(max_length=128, blank=True, verbose_name='비밀글 비밀번호')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '벼룩시장 댓글'
        verbose_name_plural = '벼룩시장 댓글'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# 25-12-29 슬기 수정: 알림 시스템 모델 추가
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications', verbose_name='수신자')
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='actions', verbose_name='발신자')
    flea_item = models.ForeignKey(FleaItem, on_delete=models.CASCADE, verbose_name='상품')
    flea_comment = models.ForeignKey(FleaComment, on_delete=models.CASCADE, null=True, blank=True, verbose_name='댓글')
    message = models.CharField(max_length=255, verbose_name='알림 메시지')
    is_read = models.BooleanField(default=False, verbose_name='읽음 여부')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성 시간')

    class Meta:
        verbose_name = '알림'
        verbose_name_plural = '알림'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.nickname}님께: {self.message}"