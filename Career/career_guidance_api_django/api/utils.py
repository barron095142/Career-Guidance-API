from django.conf import settings
from django.db.models import F
from django.utils import timezone
from .models import APICallCounter

def _limit():
    try:
        val = int(getattr(settings, "DAILY_API_LIMIT", 5))
    except Exception:
        val = 5
    return max(1, val)

def rate_status(user):
    today = timezone.localdate()
    try:
        counter = APICallCounter.objects.get(user=user, date=today)
        count = counter.count
    except APICallCounter.DoesNotExist:
        count = 0
    limit = _limit()
    remaining = max(0, limit - count)
    return {"count": count, "remaining": remaining, "limit": limit, "reached": count >= limit}

def rate_hit(user):
    today = timezone.localdate()
    counter, _ = APICallCounter.objects.get_or_create(user=user, date=today, defaults={"count": 0})
    APICallCounter.objects.filter(pk=counter.pk).update(count=F("count") + 1)
    counter.refresh_from_db()
    limit = _limit()
    remaining = max(0, limit - counter.count)
    return {"count": counter.count, "remaining": remaining, "limit": limit, "reached": counter.count >= limit}
