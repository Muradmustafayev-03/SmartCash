from django.shortcuts import render , HttpResponse
from .serializer import PurchaseSerializer
from .models import Purchase 
from rest_framework import viewsets




class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer



class BillViewSet(viewsets.ViewSet):
    
    def post(self,request):
        return HttpResponse("succes")

    def get(self,request):
        return HttpResponse("<h1>only for 'post' method </h1>")
    
