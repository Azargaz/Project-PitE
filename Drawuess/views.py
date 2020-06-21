from django.shortcuts import render
from django.http import JsonResponse, Http404
import json, os, sys, random
from .s_lib import scale
from .cnn import model
from .models import Category, Similar

def main_page(request):
    try:
        c = random.choice([category.name for category in Category.objects.all()])
        context = {'to_draw': c}
        return render(request,'main_page.html', context)
    except Exception as e:
        print(e)
        raise Http404("ERROR")

def about(request):
    try:
        return render(request,'about.html', {'items': [category.name for category in Category.objects.all()]})
    except Exception as e:
        print(e)
        raise Http404("ERROR")

def extended(request):
    return render(request,'extended.html')

def guess_image(request):
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

def get_random_similars(request, count):
    try:
        category_name = random.choice([category.name for category in Category.objects.all()])
        similars = [similar for similar in Similar.objects.filter(similar_cat_name=category_name)]
        random_sim = random.choices(similars, k=count) if len(similars) >= count else [choice(similars) for _ in range(count)]
        similar_imgs = [model.get_single_image_from_npy(random_sim[i].correct_cat_name, random_sim[i].npy_id).tolist() for i in range(len(random_sim))]        
        return JsonResponse({'pictures': json.dumps(similar_imgs),
                            'similar_to': random_sim[0].similar_cat_name },status=200)
    except Exception as e:
        print(e)
        raise Http404("ERROR")

def categories(request):
    try:
        categories = [category.name for category in Category.objects.all()]
        return JsonResponse({'categories': categories }, status=200)
    except Exception as e:
        print(e)
        raise Http404("ERROR")