from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

@api_view(['GET'])
def spending_by_month(request):
    month = request.GET.get('month')
    year = request.GET.get('year')

    if not month or not year:
        return Response({"Error: month and year required"}, status=400)
        
    transaction = Transaction.objects.filter(
        date__month = month,
        date__year = year
    )

    serializer = TransactionSerializer(transaction, many=True)
    return Response(serializer.data)
    