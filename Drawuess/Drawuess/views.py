from django.shortcuts import render
from django.http import JsonResponse, Http404
import json, os, sys
from .s_lib import scale
from .cnn import model
from random import choice
import json

from .models import Category, Similar

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
        random_sim = [choice(similars) for _ in range(4)]
        similar_img1 = model.get_single_image_from_npy(random_sim[0].correct_cat_name, random_sim[0].npy_id)
        similar_img2 = model.get_single_image_from_npy(random_sim[1].correct_cat_name, random_sim[1].npy_id)
        similar_img3 = model.get_single_image_from_npy(random_sim[2].correct_cat_name, random_sim[2].npy_id)
        similar_img4 = model.get_single_image_from_npy(random_sim[3].correct_cat_name, random_sim[3].npy_id)

        similar_img1 = similar_img1.tolist()
        similar_img2 = similar_img2.tolist()
        similar_img3 = similar_img3.tolist()
        similar_img4 = similar_img4.tolist()
        return JsonResponse({'picture1': json.dumps(similar_img1[0][0]),
                            'picture2': json.dumps(similar_img2[0][0]),
                            'picture3': json.dumps(similar_img3[0][0]),
                            'picture4': json.dumps(similar_img4[0][0]),
                            'similar_to': random_sim[0].similar_cat_name, 'category': random_sim[0].correct_cat_name },status=200)
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