from django.shortcuts import render
from ML.category_classifier import Classifier

c = Classifier()
c.train()


def home(request):
    print(c.test())
    return render(request, r"purchase.html")
