from django.http import JsonResponse
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt

from .simulation import run_economic_simulation

def index(request):
    return render(request, 'simulation/index.html')

@csrf_exempt
def run_simulation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        policies = json.loads(data.get('policies', '[]'))
        
        # Run the simulation based on policies
        results = run_economic_simulation(policies)
        
        return JsonResponse(results)
    return JsonResponse({"error": "Invalid request"}, status=400)
