from django.shortcuts import render
from django.http import JsonResponse, Http404
import json

def main_page(request):
    return render(request,'main_page.html')

def picture(request):
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(type(body))
    except Exception:
        raise Http404("ERROR") # trzeba zmienic
    else:
        return JsonResponse({'s':'s'},status=200)