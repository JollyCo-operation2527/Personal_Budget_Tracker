from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from transactions.models import Transaction, Item

def recur_payments_obj():
    today = date.today()
    start = datetime.strptime('2025-02-01', '%Y-%m-%d').date()
    # Try to add rent and phone bill for each month since Feb 2025 to today

    """ IMPORTANT NOTE: ADJUST THE CODE WHEN GETTING DIFFRENT PHONE PLANS OR DIFFERENT RENT PRICE 
    A.K.A CHANGE THE START DATE"""

    while start.month <= today.month:
        # I pay 600 every first day of the month (Rent)
        new_month_rent = Transaction(
            store_name = "Rent",
            total_amount = 600,
            date = start,
            category = "Rent"
        )
        new_month_rent.save()

        # I pay 45.20 every fifth day of the month (Phone bill)
        new_phone_bill = Transaction(
            store_name = "Chatr Mobile",
            total_amount = 45.20,
            date = start + relativedelta(days=4),
            category = "Phone/Internet"
        )
        new_phone_bill.save()
        
        # Increment month by 1
        start += relativedelta(months=1)
