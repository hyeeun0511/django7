from django.db import models

class Payment(models.Model):
    aid = models.CharField(max_length=50)  # 결제 승인 번호
    tid = models.CharField(max_length=50)  # 결제 고유 번호
    cid = models.CharField(max_length=20)  # 가맹점 코드
    order_id = models.CharField(max_length=100)  # 주문 번호
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # 결제 금액
    created_at = models.DateTimeField(auto_now_add=True)  # 결제 일시

    def __str__(self):
        return f"Payment {self.tid} for Order {self.order_id}"