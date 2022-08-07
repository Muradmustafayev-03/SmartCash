from django.shortcuts import render, HttpResponse
from .serializer import PurchaseSerializer
from .models import Purchase
from rest_framework import viewsets
from Parser.parser import parse_purchase


def home(request):
    return render(request, "purchases_data/templates/purchase.html")


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer


class BillViewSet(viewsets.ViewSet):
    @staticmethod
    def post(request):
        print(parse_purchase(request.data["user_FIN"], request.data["user_token"]))
        return HttpResponse("succes")

    @staticmethod
    def get(request):
        return HttpResponse("<h1>only for 'post' method </h1>")
