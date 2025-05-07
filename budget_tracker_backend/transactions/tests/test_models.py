import pytest
from transactions.models import Transaction, Item
from django.db import IntegrityError
from datetime import date

# Simple test
@pytest.mark.django_db
def test_transaction_creation():
    tx = Transaction.objects.create(
        store_name = "Costco",
        total_amount = 25.75,
        date = date.today(),
        category = "Groceries",
    )

    expected_val = ["Costco", 25.75, date.today(), "Groceries"]
    tx_val = [tx.store_name, tx.total_amount, tx.date, tx.category]

    assert tx_val == expected_val


# Test adding duplicate transactions
@pytest.mark.django_db
def test_no_duplicate():
    tx1 = Transaction.objects.create(
        store_name = "Costco",
        total_amount = 30,
        date = date.today(),
        category = "Groceries",
    )

    # Shouldn't be added
    with pytest.raises(IntegrityError):
        tx2 = Transaction.objects.create(
            store_name = "Costco",
            total_amount = 30,
            date = date.today(),
            category = "Groceries",
        )
        
# However, this is ok
@pytest.mark.django_db
def test_check_duplicate():
    tx1 = Transaction.objects.create(
        store_name = "Costco",
        total_amount = 30,
        date = date.today(),
        category = "Groceries",
    )

    tx2 = Transaction.objects.get_or_create(
        store_name = "Costco",
        total_amount = 30,
        date = date.today(),
        category = "Groceries",
    )
