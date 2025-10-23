from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import connection
from datetime import datetime
from django.conf import settings
import os

@api_view(['GET'])
def index(request):
    """
    Respond with current time and 200 response code.
    """
    data = {"Status": "OK", "timestamp": datetime.now().isoformat()}
    # Check database connectivity
    try:
        start_time = datetime.now()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            cursor.fetchone()
        end_time = datetime.now()
        latency = (end_time - start_time).total_seconds() * 1000  # in milliseconds
        data['database_connection'] = 'successful'
        data['database_latency_ms'] = latency
    except Exception as e:
        data['database_connection'] = 'failed'
    
    # Check Users Service connectivity
    import requests
    USERS_SERVICE_URL = settings.USERS_SERVICE_URL
    print("Checking Users Service at:", USERS_SERVICE_URL)
    try:
        start_time = datetime.now()
        response = requests.get(f"{USERS_SERVICE_URL}/health/", timeout=2)
        end_time = datetime.now()
        latency = (end_time - start_time).total_seconds() * 1000  # in milliseconds
        data['users_service_latency_ms'] = latency
        if response.status_code == 200:
            data['users_service'] = 'reachable'
        else:
            data['users_service'] = 'unreachable'
    except requests.RequestException:
        data['users_service'] = 'unreachable'

    
    return Response(data, status=200)   
