# daily_inspection/api.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DailyInspection
from django.utils import timezone

@api_view(['GET'])
def get_shift_progress(request):
    """
    Get the current progress for both shifts for today
    """
    today = timezone.now().date()
    
    day_progress = DailyInspection.calculate_shift_progress('Day', today)
    night_progress = DailyInspection.calculate_shift_progress('Night', today)
    
    return Response({
        'date': today,
        'day_shift_progress': day_progress,
        'night_shift_progress': night_progress
    })