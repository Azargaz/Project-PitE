from django.shortcuts import render
from django.http import JsonResponse, Http404
import json, os, sys
from .s_lib import scale
from .cnn import model

import json

def main_page(request):
    return render(request,'main_page.html')

def picture(request):
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        body = body.split(',')
        pic = scale.prepare_image(body[1])
        response = model.predict(pic)
        return JsonResponse({'result': str(response) }, status=200)
    except Exception as e:
        print(e)
        raise Http404("ERROR")
    else:
        return JsonResponse({'error': 'Something went wrong.'}, status=500)