from django.urls import path
from django.http import JsonResponse
from .views import (
    SignupView, LoginView,
    RateStatusView, RateHitView,
    CareerChatView, LatestNewsView,
    roadmap_api, job_market_api, skill_service, recommendation_service,
    career_service, interview_service, resume_service,
)

def api_ping(request): 
    return JsonResponse({"ok": True, "where": "api.urls"})

urlpatterns = [
    path("ping/", api_ping), 

    path("auth/signup/", SignupView.as_view(), name="signup"),
    path("auth/login/",  LoginView.as_view(),  name="login"),

    path("rate/status/", RateStatusView.as_view(), name="rate-status"),
    path("rate/hit/",    RateHitView.as_view(),    name="rate-hit"),

    path("ai/chat/", CareerChatView.as_view(), name="career-chat"),

    path("news/", LatestNewsView.as_view(), name="latest-news"),

    path("roadmap/",            roadmap_api,          name="roadmap"),
    path("job-market/",         job_market_api,       name="job-market"),
    path("skills/analyze/",     skill_service,        name="skill-service"),
    path("recommendations/",    recommendation_service, name="recommendation-service"),
    path("career/paths/",       career_service,       name="career-service"),
    path("interview/qa/",       interview_service,    name="interview-service"),
    path("resume/score/",       resume_service,       name="resume-service"),
]
