from django.contrib import admin
from .models import Transaction, Item

admin.site.register(Transaction)
admin.site.register(Item)