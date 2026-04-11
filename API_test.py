import requests
import pandas as pd
import time

class CivilServiceAPI:
    def __init__(self, service_key):
        # 파이썬 requests는 내부적으로 인코딩을 수행하므로 unquote된 키를 사용하는 것이 안전합니다.
        self.service_key = requests.utils.unquote(service_key)
        self.base_url = "http://apis.data.go.kr/B551982/cso_v2"

    def fetch_data(self, sub_url, params):
        """공통 데이터 호출 함수 (502 에러 대응)"""
        full_url = f"{self.base_url}/{sub_url}"
        default_params = {
            'serviceKey': self.service_key,
            'pageNo': '1',
            'numOfRows': '20',
            'resultType': 'json'
        }
        default_params.update(params)

        try:
            response = requests.get(full_url, params=default_params, timeout=15)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 502:
                print("⚠️ [502 Error] 공공데이터 서버가 일시적으로 응답하지 않습니다. 잠시 후 다시 시도해 주세요.")
                return None
            else:
                print(f"❌ 오류 발생 (상태 코드: {response.status_code})")
                print("응답 내용:", response.text)
                return None
        except Exception as e:
            print(f"❗ 연결 오류: {e}")
            return None

    def get_office_list(self, search_keyword=""):
        """민원실 목록 및 기본정보 조회"""
        print(f"🔍 '{search_keyword}' 관련 민원실 목록을 불러오는 중...")
        data = self.fetch_data("cso_info_v2", {})
        
        if data and 'response' in data and 'body' in data['response']:
            items = data['response']['body'].get('items', [])
            if not items:
                print("검색 결과가 없습니다.")
                return pd.DataFrame()
            return pd.DataFrame(items)[['instNm', 'addr', 'telNo']]
        return pd.DataFrame()

    def get_realtime_status(self, inst_nm):
        """특정 기관의 실시간 창구별 대기 현황 조회"""
        print(f"📊 '{inst_nm}'의 실시간 대기 현황을 조회하는 중...")
        data = self.fetch_data("cso_realtime_v2", {'instNm': inst_nm})
        
        if data and 'response' in data and 'body' in data['response']:
            items = data['response']['body'].get('items', [])
            if not items:
                print(f"'{inst_nm}'에 대한 실시간 정보가 현재 제공되지 않습니다.")
                return pd.DataFrame()
            
            # 창구명, 대기수, 호출번호 등 핵심 정보 추출
            df = pd.DataFrame(items)
            return df[['windowNm', 'waitCnt', 'callNum']] if not df.empty else df
        return pd.DataFrame()

# --- 실행부 ---
if __name__ == "__main__":
    # 1. 인증키 설정 (사용자님이 제공해주신 키)
    MY_KEY = "44ee7a331e4637a576a94b65a28033989a585455456d1fbc441b982883fc79fd"
    
    api = CivilServiceAPI(MY_KEY)

    # 2. 첫 번째 단계: 어떤 기관이 있는지 확인 (샘플 20개)
    offices = api.get_office_list()
    if not offices.empty:
        print("\n[전국 민원실 목록 샘플]")
        print(offices.head(10))
        
        # 3. 두 번째 단계: 목록에 있는 기관 중 하나를 골라 실시간 상태 확인
        # (리스트에 있는 'instNm' 중 하나를 복사해서 넣어보세요)
        target_name = offices.iloc[0]['instNm'] # 첫 번째 검색된 기관으로 자동 설정
        status = api.get_realtime_status(target_name)
        
        if not status.empty:
            print(f"\n[{target_name} 실시간 대기 현황]")
            print(status)
    else:
        print("\n데이터를 불러오지 못했습니다. 인증키 승인 대기 중이거나 서버 점검 중일 수 있습니다.")