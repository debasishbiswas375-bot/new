from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        
        # We will add the "Real Conversion Logic" here in the next step.
        # For now, let's just prove it works!
        return HttpResponse(f"✅ Received file: {uploaded_file.name}")

    return render(request, 'home.html')
