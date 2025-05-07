import pytest
from transactions.views import TransactionViewSet
from rest_framework.test import APIClient
from django.urls import reverse
from datetime import date
from transactions.models import Transaction, Item

# Simple post test
@pytest.mark.django_db
def test_views():
    client = APIClient()
    url = reverse("transaction-list")
    data = {
        "store_name": "Costco",
        "total_amount": 50,
        "date": date.today(),
        "category": "Groceries",
    }
    response = client.post(url, data, format="json")

    assert response.status_code == 201
    assert Transaction.objects.count() == 1

    expected_val = ["Costco", 50, date.today(), "Groceries"]
    tx_val = [Transaction.objects.first().store_name, Transaction.objects.first().total_amount, 
    Transaction.objects.first().date, Transaction.objects.first().category]

    assert tx_val == expected_val

# spending_by_month test
@pytest.mark.django_db
def test_spending_by_month():
    client = APIClient()
    Transaction.objects.create(
        store_name = "Costco",
        total_amount = 100,
        date = "2025-01-01",
        category = "Groceries",
    )
    url = reverse("spending_by_month")

    response = client.get(url, {"month": 1, "year": 2025})

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0].get('store_name') == "Costco"
    assert data[0].get('total_amount') == 100
    assert data[0].get('date') == "2025-01-01"
    assert data[0].get('category') == "Groceries"
        
    


    
    


    