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
    pass

def confirmation(request):
    """
    Confirmation view

    """
    pass



