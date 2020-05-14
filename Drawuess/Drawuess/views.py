from django.shortcuts import render
from django.http import JsonResponse, Http404
import json, os, sys
from .settings import BASE_DIR
file = os.path.join(BASE_DIR,'s_lib')
sys.path.insert(1, file)
import scale



def main_page(request):
    return render(request,'main_page.html')

def picture(request):
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        body = body.split(',')
        pic = scale.scale_picture_arr(body[1])
    except Exception:
        raise Http404("ERROR") # trzeba zmienic
    else:
        return JsonResponse({'s':'s'},status=200)