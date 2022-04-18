from django.shortcuts import render

# Create your views here.

def test_view(req):
    return render(req,"ticket.html")
