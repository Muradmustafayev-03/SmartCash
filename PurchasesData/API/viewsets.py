from django.shortcuts import HttpResponse
from PurchasesData.API.serializers import PurchaseSerializer
from PurchasesData.models import Purchase, User
from rest_framework import viewsets
from Parsers.e_kassa_parser import parse_purchase, write_to_db
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 20

class PurchaseViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseSerializer
    pagination_class = LargeResultsSetPagination
    
    @action(detail=False, methods=['get'])
    def get_queryset(self):
        return Purchase.objects.filter(**self.request.data)
    
        
class BillViewSet(viewsets.ViewSet):
    @staticmethod
    def post(request):
        purchase_info = parse_purchase(request.data['user_FIN'], request.data['user_token'])
        write_to_db(purchase_info)
        return HttpResponse('success')

    @staticmethod
    def get(request):
        return HttpResponse("<div style='width: 100%; height: 100%; display:flex;align-items: center; "
                            "justify-content: center; font-size: 50px; color: black;'>"
                            "<p>only for POST method</p></div>")
