from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    user = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    deleteYN = models.CharField(max_length=1, default='N')
    delete_dt = models.DateTimeField(null=True, blank=True)  # 수정된 부분

    def __str__(self):
        return self.title
    
    
class StockData(models.Model):
    symbol = models.CharField(max_length=10)  # 주식 심볼
    price = models.FloatField()  # 현재 가격
    volume = models.FloatField(null=True, blank=True) 
    timestamp = models.DateTimeField(auto_now_add=True)  # 데이터 저장 시간

    def __str__(self):
        return self.symbol