from django.shortcuts import render
from django.http import HttpResponse

def main_page(request):
    return render(request,'main_page.html')

# def picture(request, obraz):
#     print("Jestem tutaj !!!!!!!!!!!!!!!!!!")
#     return HttpReponse({'s':'s'},mimetype='application/json')