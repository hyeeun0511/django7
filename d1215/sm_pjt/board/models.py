from django.db import models
from member.models import Member

class Board(models.Model):
    bno = models.AutoField(primary_key=True)
    # id -> ORM방식 객체저장이 가능해짐
    member = models.ForeignKey(Member,on_delete=models.DO_NOTHING,null=True)   # Member에 있는 models의 ForeignKey를 갖고옴  # id만 갖고오는것이 아닌 => 회원정보 전체를 가져옴
    # on_delete=models.DO_NOTHING : 아무 행동을 하지 않음
    # models.CASCADE : 외래키삭제할때 외래키를 포함하는 행도 함께 삭제
    # models.SET_NULL : 외래키 값을 NULL값으로 변경(null=True일때 사용 가능)
    btitle = models.CharField(max_length=1000)
    bcontent = models.TextField()
    bgroup = models.IntegerField(default=0)
    bstep = models.IntegerField(default=0)
    bindent = models.IntegerField(default=0)
    bhit = models.IntegerField(default=0)
    bfile = models.CharField(max_length=100,default='')        # 파일첨부  # 빈공백('')이 디폴트(default)값
    bdate = models.DateTimeField(auto_now=True)
    
    # 답변달기 사용에 필요한 컬럼
    # bgroup,bstep,bindent  : 얘네를 추가해야 답변을 달수있음
    # 파일첨부
    # bfile
    
    def __str__(self):
        return f'{self.bno},{self.btitle},{self.member.id},{self.bdate}'