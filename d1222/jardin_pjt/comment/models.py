from django.db import models
from customer.models import Board
from member.models import Member
from django.utils import timezone

class Comment(models.Model):
    cno = models.AutoField(primary_key=True)
    board = models.ForeignKey(Board,on_delete=models.CASCADE)
    member = models.ForeignKey(Member,on_delete=models.SET_NULL,null=True,blank=True)
    cpw = models.CharField(max_length=10,null=True,blank=True)
    ccontent = models.TextField(blank=True)
    cdate = models.DateTimeField(auto_now=True,null=True,blank=True)
    
    def __str__(self):
        return f'{self.cno},{self.board.bno},{self.member.id},{self.cpw},{self.ccontent},{self.cdate}'
