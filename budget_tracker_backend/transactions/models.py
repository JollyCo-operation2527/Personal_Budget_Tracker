from django.db import models

class Transaction(models.Model):
    store_name = models.CharField(max_length=30)
    total_amount = models.FloatField()
    date = models.DateField()
    category = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.store_name} - ${self.total_amount} on {self.date}"

class Item(models.Model):
    transaction = models.ForeignKey(Transaction, related_name='items', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=50)
    price = models.FloatField()
    sub_category = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.item_name} - ${self.price} from {self.transaction}"


