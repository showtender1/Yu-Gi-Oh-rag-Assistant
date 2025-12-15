import os

GOOGLE_API_KEY = os.getenv("AIzaSyBskbIDFZYy5mtl5xgqNo3eAfHGyJq-5AQ")

if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY 환경변수가 설정되지 않았습니다.")
