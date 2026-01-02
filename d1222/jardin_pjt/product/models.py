from django.db import models

class Payment(models.Model):
    aid = models.CharField(max_length=30,null=True,blank=True)
    tid = models.CharField(max_length=30,null=True,blank=True)
    cid = models.CharField(max_length=20,default='0')

    partner_order_id = models.CharField(max_length=100,null=True,blank=True)
    partner_user_id = models.CharField(max_length=100,null=True,blank=True)

    payment_method_type = models.CharField(max_length=20,null=True,blank=True)

    item_name = models.CharField(max_length=100,null=True,blank=True)
    # 0 이상(양수) 정수만 저장 가능한 필드
    quantity = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.item_name},{self.tid}"
    
class PaymentAmount(models.Model):
   # 1 : 1 관계 - 하나의 Payment 와만 연결 
   payment = models.OneToOneField(
        Payment,
        on_delete=models.CASCADE,
        related_name="amount"  # 역방향 참조
    )
   total = models.PositiveIntegerField(default=0)
   tax_free = models.PositiveIntegerField(default=0)
   vat = models.PositiveIntegerField(default=0)
   point = models.PositiveIntegerField(default=0)
   discount = models.PositiveIntegerField(default=0)
   green_deposit = models.PositiveIntegerField(default=0)

   def __str__(self):
       return f"{self.total}"

