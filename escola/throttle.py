from rest_framework.throttling import UserRateThrottle

class MatriculaUserRateThrottle(UserRateThrottle):
    rate = "20/day"
