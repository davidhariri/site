import os
from posthog import Posthog
from flask import request
from functools import wraps

posthog = Posthog(project_api_key=os.getenv("POSTHOG_KEY"), host='https://app.posthog.com')
posthog.api_key = os.getenv("POSTHOG_KEY")

def track_request(func):
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        if posthog.api_key is None:
            return func(*args, **kwargs)
        
        x_forwarded_for = request.headers.get('X-Forwarded-For')
        
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.remote_addr

        posthog.capture(
            ip_address,
            '$pageview', {'$current_url': request.url, '$referrer': request.referrer},
            disable_geoip=False,
        )

        return func(*args, **kwargs)
    return wrapper
