from django.shortcuts import render

from . import functions

def day_selector(request):
    """
    Day selector view

    """
    return render(request,"appointment/day_selector.html")

def slot_selector(request):
    """
    Slot selector view

    """
    day = request.POST["day"]
    
    return render(request,"appointment/slot_selector.html")

def confirmation(request):
    """
    Confirmation view

    """
    pass



