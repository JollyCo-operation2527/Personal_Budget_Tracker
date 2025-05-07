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
