from django.shortcuts import render
from ML.category_classifier import SimpleClassifier

c = SimpleClassifier()
c.train()


def home(request):
    print(c.test())
    return render(request, r"purchase.html")
