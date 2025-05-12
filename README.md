To whomever find this project:
    This app was made for myself to track my monthly spending.
    There are only couple of places I spend my money on that provide e-receipts.
    The idea of the app is reading the online receipts sent to my gmail inbox,
    then extract the relevant information (date, total amount, store), save them in the database
    then display it via frontend (using rechart)

    To use this app, one must get credentials.json from google API (to allow the app to read emails from inbox)
    Since each vendor has different ways to format their receipt, I must have different case for each store.
    For now, only Steam, Food Basics, and DOmino's Pizza send me e-receipt. Everything else will have to be entered manually.


run test:
  cd ~/Budget_Tracker/budget_tracker_backend
  pytest

run gmail_reader:
  cd ~/Budget_Tracker/budget_tracker_backend
  python -m transactions.services.gmail_reader

run backend:
  python manage.py runserver

run frontend:
  npm run dev


Note to self: remember the secret/ 
