import requests
import pandas as pd

# 1. 정보 설정
endpoint = "https://apis.data.go.kr/B551982/cso_v2/cso_info_v2" # 민원실 기본정보 주소
service_key = "44ee7a331e4637a576a94b65a28033989a585455456d1fbc441b982883fc79fd"

# 2. 요청 파라미터 (서버에 보낼 질문지)
params = {
    'serviceKey': service_key,
    'pageNo': '1',          # 첫 번째 페이지
    'numOfRows': '10',      # 10개만 가져오기
    'resultType': 'json'    # 결과를 JSON 형식으로 받기
}

try:
    # 3. API 호출
    response = requests.get(endpoint, params=params)
    
    # 4. 결과 확인
    if response.status_code == 200:
        data = response.json()
        
        # 데이터 구조가 복잡할 수 있으니 핵심 아이템만 추출
        if 'response' in data and 'body' in data['response']:
            items = data['response']['body']['items']
            df = pd.DataFrame(items)
            
            print("✅ 연동 성공! 데이터 샘플:")
            print(df[['instNm', 'addr', 'telNo']]) # 기관명, 주소, 전화번호만 출력
        else:
            print("⚠️ 호출은 성공했으나 데이터가 비어있습니다. (승인 대기 중일 수 있음)")
            print("응답 내용:", data)
    else:
        print(f"❌ 연동 실패 (상태 코드: {response.status_code})")

except Exception as e:
    print(f"❗ 오류 발생: {e}")