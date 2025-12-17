from django.db import models
from board.models import Board
from member.models import Member

class Comment(models.Model):
    cno = models.AutoField(primary_key=True)  # 댓글번호
    board = models.ForeignKey(Board,on_delete=models.CASCADE)  # 댓글 게시글 번호  # cascade:부모댓글 사라지면 같이 사라짐, SET_NULL
    member = models.ForeignKey(Member,on_delete=models.SET_NULL, null=True, blank=True)  # 댓글 작성자 번호
    cpw = models.CharField(max_length=10,null=True, blank=True)  # 비밀글
    ccontent = models.TextField()  # 댓글 내용
    cdate = models.DateTimeField(auto_now=True)  # 댓글 작성일,시간  # 수정할때마다 현재 시간으로 자동 설정
    
    
    
    def __str__(self):
        return f'{self.cno},{self.board.bno},{self.member.id},{self.cpw},{self.ccontent},{self.cdate}'
    