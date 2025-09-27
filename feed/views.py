from django.http import JsonResponse
from django.shortcuts import render

def index(request):
    return JsonResponse({
        'message': 'Social Media Feed Backend API',
        'graphql_endpoint': '/graphql/',
        'status': 'running'
    })

def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'service': 'social_media_feed',
    })
