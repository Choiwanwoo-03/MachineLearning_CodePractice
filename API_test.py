import requests
import json

SERVICE_KEY = "44ee7a331e4637a576a94b65a28033989a585455456d1fbc441b982883fc79fd"
BASE_URL    = "https://apis.data.go.kr/B551982/cso_v2/cso_realtime_v2"
BJDONG_CODE = "4413310300"

# serviceKey는 URL에 직접 붙이기 (인코딩 문제 방지)
url = f"{BASE_URL}?serviceKey={SERVICE_KEY}"

params = {
    "bjdongCode": BJDONG_CODE,
    "type":       "json",
    "numOfRows":  100,
    "pageNo":     1,
}

try:
    response = requests.get(url, params=params, timeout=30)  # 타임아웃 30초로 증가
    print("상태코드:", response.status_code)
    print("Content-Type:", response.headers.get("Content-Type"))
    print("응답 원문 (앞 1000자):")
    print(response.text[:1000])  # 일단 raw 텍스트로 확인
except requests.exceptions.Timeout:
    print("❌ 타임아웃 - 서버 응답 없음")
except requests.exceptions.RequestException as e:
    print(f"❌ 요청 오류: {e}")