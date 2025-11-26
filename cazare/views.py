from django.shortcuts import render

# Aceasta este functia pentru pagina principala
def homepage(request):
    return render(request, 'cazare/homepage.html')