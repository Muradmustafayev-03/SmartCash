from django.shortcuts import render, HttpResponse
from .serializer import PurchaseSerializer
from .models import Purchase, User
from rest_framework import viewsets
from Parsers.e_kassa_parser import parse_purchase, write_to_db
from rest_framework.decorators import action


def home(request):
    return render(request, 'purchase.html')


class PurchaseViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseSerializer
    
    @action(detail=False, methods=['get'])
    def get_queryset(self):
        user = User.objects.select_related('purchases').all()
        return Purchase.objects.filter(**self.request.data)


class BillViewSet(viewsets.ViewSet):
    @staticmethod
    def post(request):
        user_ifo = parse_purchase(request.data['user_FIN'], request.data['user_token'])
        write_to_db(user_ifo)
        return HttpResponse('success')

    @staticmethod
    def get(request):
        return HttpResponse("<div style='width: 100%; height: 100%; display:flex;align-items: center; "
                            "justify-content: center; font-size: 50px; color: black;'>"
                            "<p>only for POST method</p></div>")
