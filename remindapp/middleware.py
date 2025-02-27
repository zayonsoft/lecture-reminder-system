# middleware.py
from datetime import timedelta
from django.utils.timezone import now

class RefreshSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            # Extend session expiry on activity
            one_hour = 60*60
            request.session.set_expiry(now() + timedelta(seconds=one_hour))  # Extend by 1 hour
        return response
