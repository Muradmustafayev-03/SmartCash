from django.shortcuts import render
from ML.category_classifier import SimpleClassifier

c = SimpleClassifier()


def home(request):
    print(c.avg_precision())
    return render(request, r"purchase.html")
