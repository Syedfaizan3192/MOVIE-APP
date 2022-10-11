from rest_framework.throttling import UserRateThrottle


# Custom Throttling
class ReviewListThrottle(UserRateThrottle):
    scope = 'reviewlist'
