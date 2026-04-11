import requests
from urllib.parse import quote

SERVICE_KEY = "44ee7a331e4637a576a94b65a28033989a585455456d1fbc441b982883fc79fd"
ENCODED_KEY = quote(SERVICE_KEY, safe='')  # URL 인코딩

BASE_URL    = "https://apis.data.go.kr/B551982/cso_v2/cso_realtime_v2"
BJDONG_CODE = "4413310300"

url = f"{BASE_URL}?serviceKey={ENCODED_KEY}&bjdongCode={BJDONG_CODE}&type=json&numOfRows=10&pageNo=1"

print("호출 URL:")
print(url)
print()

try:
    response = requests.get(url, timeout=60)
    print("상태코드:", response.status_code)
    print("응답 원문:")
    print(response.text[:1000])
except requests.exceptions.Timeout:
    print("❌ 타임아웃")
except requests.exceptions.RequestException as e:
    print(f"❌ 오류: {e}")