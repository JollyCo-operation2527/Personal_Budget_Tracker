import pytest
from transactions.serializers import TransactionSerializer
from datetime import date

# Simple test
@pytest.mark.django_db
def test_serializer():
    data = {"store_name": "Costco", "total_amount": 50, "date": date.today(), "category": "Groceries"}
    serializer = TransactionSerializer(data=data)
    assert serializer.is_valid()
    tx = serializer.save()
    assert tx.store_name == "Costco", tx.total_amount == 50
    assert tx.date == date.today(), tx.category == "Groceries"

# Duplicate test 
@pytest.mark.django_db
def test_serializer_duplicate():
    data = {"store_name": "Costco", "total_amount": 50, "date": date.today(), "category": "Groceries"}
    serializer1 = TransactionSerializer(data=data)
    serializer2 = TransactionSerializer(data=data)
    assert serializer1.is_valid()
    tx1 = serializer1.save()

    with pytest.raises(AssertionError):
        assert serializer2.is_valid()
    


    