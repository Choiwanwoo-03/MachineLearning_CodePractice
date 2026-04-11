import requests
import pandas as pd

def get_specific_realtime_status():
    # 1. 정보 설정 (사용자 제공 데이터)
    url = "https://apis.data.go.kr/B551982/cso_v2/cso_realtime_v2"
    service_key = "44ee7a331e4637a576a94b65a28033989a585455456d1fbc441b982883fc79fd"
    stdg_cd = "4413310300" # 천안시 불당동 주변 지자체 코드

    # 2. 파라미터 구성
    params = {
        'serviceKey': requests.utils.unquote(service_key), # 인증키 특수문자 처리
        'stdgCd': stdg_cd,
        'pageNo': '1',
        'numOfRows': '10',
        'resultType': 'json'
    }

    print(f"🚀 요청 URL: {url}?stdgCd={stdg_cd}")
    
    try:
        # 3. API 호출 (타임아웃을 30초로 늘려 서버 응답을 기다립니다)
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # 4. 데이터 파싱 및 출력
            body = data.get('response', {}).get('body', {})
            items = body.get('items', [])
            
            if items:
                df = pd.DataFrame(items)
                print("\n✅ [실시간 대기 현황 데이터]")
                # 필요한 컬럼만 선택해서 보여줍니다
                cols = ['instNm', 'windowNm', 'waitCnt', 'callNum']
                print(df[cols] if all(c in df.columns for c in cols) else df)
                return df
            else:
                print("\n⚠️ 현재 해당 지역에 운영 중인 실시간 대기 창구가 없습니다.")
                print("응답 내용:", data)
        else:
            print(f"❌ 서버 응답 오류 (코드: {response.status_code})")
            print("상세 메시지:", response.text)

    except requests.exceptions.Timeout:
        print("❗ [Timeout] 서버 대답이 너무 늦습니다. 주말 점검 중일 확률이 매우 높습니다.")
    except Exception as e:
        print(f"❗ 오류 발생: {e}")

# 실행
if __name__ == "__main__":
    get_specific_realtime_status()