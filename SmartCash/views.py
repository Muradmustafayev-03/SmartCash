from django.shortcuts import render
from Parsers.bazarstore_parser import write_to_db


def home(request):
    write_to_db()
    return render(request, r"purchase.html")
