from django.shortcuts import render
from django.http import JsonResponse, Http404
import json, os, sys
from .s_lib import scale
from .cnn import model
from random import choice
import json

from .models import Category, Similar

# from PIL import Image

def main_page(request):
    c = choice([category.name for category in Category.objects.all()])
    context = {'to_draw':c}
    return render(request,'main_page.html',context)

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

def picture_extended(request):
    try:
        category_name = choice([category.name for category in Category.objects.all()])
        similars = [similar for similar in Similar.objects.filter(similar_cat_name=category_name)]
        random_sim = choice(similars)
        similar_img = model.get_single_image_from_npy(random_sim.correct_cat_name, random_sim.npy_id)
        # Image.fromarray(similar_img[0][0] * 255).show()
        similar_img = similar_img.tolist()
        return JsonResponse({'picture': json.dumps(similar_img[0][0]), 'similar_to': random_sim.similar_cat_name, 'category': random_sim.correct_cat_name }, status=200)
    except Exception as e:
        print(e)
        raise Http404("ERROR")
    else:
        return JsonResponse({'error': 'Something went wrong.'}, status=500)

def categories(request):
    categories = [category.name for category in Category.objects.all()]
    return JsonResponse({'categories': categories }, status=200)
    
def random_similar(request, category_name):
    similars = [similar for similar in Similar.objects.filter(similar_cat_name=category_name)]
    random_sim = choice(similars)
    try:
        similar_img = model.get_single_image_from_npy(random_sim.correct_cat_name, random_sim.npy_id)
        Image.fromarray(similar_img[0][0] * 255).show()
        similar_img = similar_img.tolist()
        return JsonResponse({'similar': json.dumps(similar_img[0][0]) }, status=200)
    except Exception as e:
        print(e)
        raise Http404("ERROR")
    else:
        return JsonResponse({'error': 'Something went wrong.'}, status=500)

def about(request):
    return render(request,'about.html',{'items': [category.name for category in Category.objects.all()]})

def extended(request):
    return render(request,'extended.html')