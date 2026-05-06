from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from .models import Transaction
from .serializers import TransactionSerializer

# Create your views here.
class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class TransactionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    lookup_field = 'id'

