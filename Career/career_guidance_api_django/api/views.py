import requests
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignupSerializer
from .utils import rate_status, rate_hit

User = get_user_model()

class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Signup successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response({"error": "username and password are required"}, status=400)
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"error": "Invalid credentials"}, status=401)
        refresh = RefreshToken.for_user(user)
        return Response({"access": str(refresh.access_token), "refresh": str(refresh)})


class RateStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request): return Response(rate_status(request.user))

class RateHitView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request): return Response(rate_hit(request.user))

import requests
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignupSerializer
from .utils import rate_status, rate_hit

User = get_user_model()

class CareerChatView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        st = rate_status(request.user)
        if st.get("reached"):
            return Response({"error": "Daily limit reached", **st}, status=429)

        user_input = (request.data or {}).get("query")
        if not user_input:
            return Response({"error": "query is required"}, status=400)

        if not settings.OPENROUTER_API_KEY:
            return Response({"error": "OPENROUTER_API_KEY missing in settings"}, status=500)
        if not settings.OPENROUTER_MODEL:
            return Response({"error": "OPENROUTER_MODEL missing in settings"}, status=500)

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": settings.OPENROUTER_MODEL,
            "messages": [
                {"role": "system", "content": "You are a helpful AI career advisor for Australia. Be concise and practical."},
                {"role": "user", "content": user_input},
            ],
        }
        

        try:
            r = requests.post(url, headers=headers, json=payload, timeout=45)
        except Exception as e:
            return Response({"error": f"Network error contacting OpenRouter: {str(e)}"}, status=502)

        if r.status_code != 200:
            err_obj = {}
            try:
                j = r.json() or {}
                e = j.get("error")
                if isinstance(e, dict):
                    err_obj = e
                elif isinstance(e, str):
                    err_obj = {"message": e}
                else:
                    err_obj = {"message": (r.text or "").strip()[:400]}
            except Exception:
                err_obj = {"message": (r.text or "").strip()[:400]}

            return Response(
                {"error": "OpenRouter error", "status": r.status_code, **err_obj},
                status=r.status_code,
            )

        data = {}
        try:
            data = r.json() or {}
        except Exception:
            return Response({"error": "Invalid JSON from OpenRouter"}, status=502)

        choices = data.get("choices") or []
        choice0 = choices[0] if choices else {}
        if choice0 is None:
            choice0 = {}

        msg = choice0.get("message") or {}
        reply = msg.get("content")
        if not reply:
            return Response({"error": "No valid response received from model", "raw": data}, status=502)

        # 4) count usage
        hit = rate_hit(request.user)
        return Response({"response": reply, "usage": hit}, status=200)

class LatestNewsView(APIView):
    permission_classes = [permissions.AllowAny] 

    def get(self, request):
        url = (
            "https://newsapi.org/v2/top-headlines?"
            "sources=abc-news-au&"
            f"apiKey={settings.NEWS_API_KEY}"
        )
        try:
            res = requests.get(url, timeout=20)
            data = res.json()
            articles = [
                {
                    "title": a.get("title"),
                    "description": a.get("description"),
                    "url": a.get("url"),
                    "source": (a.get("source") or {}).get("name"),
                }
                for a in (data.get("articles") or [])
            ]
            return Response({"news": articles})
        except Exception as e:
            return Response({"error": str(e)}, status=500)


@api_view(["GET"])
def roadmap_api(request):
    role = request.query_params.get("role", "software engineer")
    data = {
        "role": role,
        "roadmap": [
            {"stage": "Assess", "items": ["Self-evaluate skills", "Identify gaps", "Pick a target role"]},
            {"stage": "Upskill", "items": ["Do 2 micro-courses", "Build 1 mini project", "Get feedback"]},
            {"stage": "Apply", "items": ["Refine resume", "Tailor cover letters", "Apply to 5 roles/week"]},
        ],
    }
    return Response(data)

@api_view(["GET"])
def job_market_api(request):
    city = request.query_params.get("city", "Sydney")
    role = request.query_params.get("role", "software engineer")
    return Response({
        "city": city,
        "role": role,
        "summary": "Stubbed market snapshot",
        "metrics": {"openings_estimate": 1200, "avg_salary_aud": 125000, "trend": "steady"},
    })

@api_view(["POST"])
def skill_service(request):
    text = (request.data or {}).get("text", "")
    KNOWN = ["python", "java", "django", "react", "sql", "aws", "gcp", "docker", "kubernetes"]
    found = sorted({s for s in KNOWN if s.lower() in text.lower()})
    return Response({"skills_detected": found, "note": "stubbed extractor"})

@api_view(["GET"])
def recommendation_service(request):
    skills = [s.strip() for s in request.query_params.get("skills", "").split(",") if s.strip()]
    recs = [
        {"title": "Build a portfolio site", "reason": "Showcase skills to employers"},
        {"title": "Do 2 mock interviews", "reason": "Improve confidence"},
        {"title": "Network weekly", "reason": "Referrals boost call-backs"},
    ]
    return Response({"based_on_skills": skills, "recommendations": recs})

@api_view(["GET"])
def career_service(request):
    skills = [s.strip() for s in request.query_params.get("skills", "").split(",") if s.strip()]
    paths = [
        {"path": "Backend Engineer", "fit_score": 0.84},
        {"path": "Full‑stack Engineer", "fit_score": 0.81},
        {"path": "Data Engineer", "fit_score": 0.72},
    ]
    return Response({"skills": skills, "paths": paths})

@api_view(["POST"])
def interview_service(request):
    role = (request.data or {}).get("role", "software engineer")
    qa = [
        {"q": "Tell me about yourself", "a": "Give a crisp 90‑second story with outcomes."},
        {"q": "A time you handled conflict?", "a": "Describe context, your action, measurable impact."},
    ]
    return Response({"role": role, "qa_samples": qa})

@api_view(["POST"])
def resume_service(request):
    text = (request.data or {}).get("text", "")
    score = min(100, 40 + len(text) // 30) 
    tips = ["Start bullets with verbs", "Quantify outcomes", "Keep to 1–2 pages"]
    return Response({"score": score, "tips": tips})
