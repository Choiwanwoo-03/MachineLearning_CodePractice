import requests
import json

# ──────────────────────────────────────────
# 설정
# ──────────────────────────────────────────
SERVICE_KEY  = "44ee7a331e4637a576a94b65a28033989a585455456d1fbc441b982883fc79fd"
BASE_URL     = "https://apis.data.go.kr/B551982/cso_v2/cso_realtime_v2"
BJDONG_CODE  = "4413310300"   # 법정동코드

params = {
    "serviceKey": SERVICE_KEY,
    "bjdongCode":  BJDONG_CODE,
    "type":        "json",      # JSON 응답 요청
    "numOfRows":   100,         # 한 번에 가져올 행 수 (필요 시 조정)
    "pageNo":      1,
}

# ──────────────────────────────────────────
# API 호출
# ──────────────────────────────────────────
def fetch_cso_data(params: dict) -> dict | None:
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()

        # 응답이 XML로 올 경우 대비 Content-Type 확인
        content_type = response.headers.get("Content-Type", "")
        if "xml" in content_type:
            print("⚠️  XML 응답이 반환됐습니다. type=json 파라미터가 무시된 것 같습니다.")
            print(response.text[:500])
            return None

        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print(f"❌ 요청 실패: {e}")
        return None
    except json.JSONDecodeError:
        print("❌ JSON 파싱 실패. 원본 응답:")
        print(response.text[:500])
        return None


# ──────────────────────────────────────────
# 실행
# ──────────────────────────────────────────
def main():
    print(f"📡 API 호출 중... (법정동코드: {BJDONG_CODE})")
    print(f"   URL: {BASE_URL}")
    print(f"   params: {params}\n")

    data = fetch_cso_data(params)
    if data is None:
        return

    # ── 전체 응답 출력 ──
    print("=" * 60)
    print("✅ 전체 응답 (JSON)")
    print("=" * 60)
    print(json.dumps(data, ensure_ascii=False, indent=2))

    # ── 응답 구조에서 items 추출 (공공데이터 포털 공통 구조 가정) ──
    try:
        items = (
            data.get("response", {})
                .get("body", {})
                .get("items", {})
                .get("item", [])
        )
        if isinstance(items, dict):   # 단일 아이템이면 리스트로 변환
            items = [items]

        if not items:
            print("\nℹ️  items가 비어있습니다. 응답 구조를 확인하세요.")
            return

        print(f"\n✅ 파싱된 데이터: 총 {len(items)}건\n")
        for idx, item in enumerate(items, 1):
            print(f"[{idx}]")
            for key, value in item.items():
                print(f"  {key}: {value}")
            print()

    except AttributeError:
        print("\n⚠️  예상과 다른 응답 구조입니다. 전체 JSON을 참고해 파싱 로직을 수정하세요.")


if __name__ == "__main__":
    main()