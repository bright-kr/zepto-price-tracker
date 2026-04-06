# Zepto Price Tracker

[![Bright Data](https://img.shields.io/badge/Powered%20by-Bright%20Data-blue?style=flat-square)](https://brightdata.co.kr)
[![Zepto Price Tracker](https://img.shields.io/badge/Zepto%20Price%20Tracker-Managed%20Solution-orange?style=flat-square)](https://brightdata.co.kr/products/insights/price-tracker/zepto)
[![Python](https://img.shields.io/badge/Python-3.9%2B-yellow?style=flat-square)](https://python.org)

[![Bright Insights Price Tracker](https://raw.githubusercontent.com/danielshashko/bright-insights-assets/main/price-tracker-hero-v2.png)](https://brightdata.co.kr/products/insights/price-tracker/zepto)

실시간 Zepto 가격 추적 - 인도의 즉시 식료품 배송 플랫폼입니다. 시작하는 방법은 두 가지입니다: **완전 관리형** 인텔리전스 플랫폼 또는 Bright Data의 AI Scraper Builder로 구축한 **커스텀 scraper**.

---

## 옵션 1: Bright Insights - AI 기반 가격 추적 (권장)

**[Bright Insights](https://brightdata.co.kr/products/insights/price-tracker/zepto)**는 Bright Data의 완전 관리형 리테일 인텔리전스 플랫폼입니다. scraper를 구축할 필요도, 인프라를 유지할 필요도 없습니다. 구조화되고 분석 준비가 완료된 가격 데이터가 대시보드, 데이터 피드 또는 BI 도구로 바로 제공됩니다.

**팀이 Bright Insights를 선택하는 이유:**
- 🚀 **설정 불필요** - 바로 사용할 수 있는 대시보드와 데이터 피드로 몇 분 안에 시작
- 🤖 **AI 기반 추천** - 대화형 AI assistant가 수백만 개의 데이터 포인트를 즉시 실행 가능한 인사이트로 전환
- ⚡ **실시간 모니터링** - 시간 단위부터 일 단위까지의 refresh 주기와 즉시 알림(email, Slack, webhook)
- 🌍 **무제한 확장성** - 모든 웹사이트, 모든 지역, 모든 refresh 빈도 지원
- 🔗 **Plug-and-play 통합** - AWS, GCP, Databricks, Snowflake 등 지원
- 🛡️ **완전 관리형** - Bright Data가 schema 변경, 사이트 업데이트, 데이터 품질을 자동으로 처리

**주요 사용 사례:**
- ✅ Zepto의 카테고리 전반에서 **식료품 가격 인플레이션 추적**
- ✅ **프로모션 모니터링** 및 주간 딜 자동 추적
- ✅ 장바구니 분석을 위한 **가격 이력 데이터베이스 구축**
- ✅ MAP 정책 준수 모니터링 및 가격 위반 감지
- ✅ 경쟁사 프로모션 및 프로모션 동향 추적
- ✅ 정제되고 표준화된 데이터를 동적 가격 책정 알고리즘 또는 AI 모델에 직접 공급

> **월 $250부터 - [맞춤 견적 받기 →](https://brightdata.co.kr/products/insights/price-tracker/zepto)**

---

## 옵션 2: 직접 Zepto Scraper 구축하기

사전 구축된 Zepto scraper API가 없나요? 문제없습니다. Bright Data의 **AI Scraper Builder**가 몇 번의 클릭만으로 커스텀 Zepto scraper를 생성합니다 — 코딩이 필요 없습니다.

### 몇 분 만에 Zepto scraper 구축하기

**[Zepto AI Scraper Builder 열기 →](https://brightdata.co.kr/products/web-scraper/zepto)**

도메인을 선택하고, 필요한 데이터를 설명하면, AI scraper builder가 API를 자동으로 생성합니다.

1. **일반적인 영어로 데이터 요구사항 설명**
2. **AI가 즉시 scraper API 생성**
3. **API 요청 실행 후 즉시 결과 확인**
4. 필요 시 **내장 IDE에서 코드 수정**

구축이 완료되면 scraper에 **Web Scraper ID**(`gd_xxxxxxxxxxxx`)가 부여됩니다 — 아래 Setup 단계에서 사용할 수 있도록 복사해 두세요.

### 사전 요구사항

- Python 3.9 이상
- [Bright Data account](https://brightdata.co.kr) (free trial 제공)
- Bright Data **API token** ([발급 방법](https://docs.brightdata.co.kr/general/account/account-settings#api-token))
- Zepto용 **Web Scraper ID** (위의 build 단계에서 획득)

### Setup

1. **이 repository clone**

   ```bash
   git clone https://github.com/bright-kr/zepto-price-tracker.git
   cd zepto-price-tracker
   ```

2. **dependencies 설치**

   ```bash
   pip install -r requirements.txt
   ```

3. **credentials 구성**

   `.env.example`을 `.env`로 복사한 뒤 값을 입력하세요:

   ```bash
   cp .env.example .env
   ```

   ```env
   BRIGHTDATA_API_TOKEN=your_api_token_here
   BRIGHTDATA_DATASET_ID=your_dataset_id_here
   ```

   > **Your Web Scraper ID**
   > [AI Scraper Builder dashboard](https://brightdata.co.kr/products/web-scraper/zepto)에서 Web Scraper ID를 복사해
   > `BRIGHTDATA_DATASET_ID`에 붙여 넣으세요 (형식: `gd_xxxxxxxxxxxx`).

---

## 사용법

Zepto scraper를 구축하고 `.env`에 Web Scraper ID를 설정하면, Python 인터페이스는 동일한 방식으로 동작합니다:

### 1. URL로 특정 상품 추적

구조화된 가격 데이터를 가져오기 위해 Zepto 상품 URL 목록을 전달합니다:

```python
from price_tracker import track_prices

urls = [
    "https://www.zeptonow.com/products/sample-product",
    # Add more product URLs here
]

results = track_prices(urls)
for item in results:
    print(f"{item.get('title')} - {item.get('final_price', item.get('price'))} {item.get('currency', '')}")
```

또는 직접 실행:

```bash
python price_tracker.py
```

### 2. 키워드로 상품 검색

키워드 검색과 일치하는 상품을 찾습니다:

```python
from price_tracker import discover_by_keyword

results = discover_by_keyword("laptop", limit=50)
```

### 3. 카테고리 URL로 상품 탐색

Zepto 카테고리 페이지의 모든 상품을 수집합니다:

```python
from price_tracker import discover_by_category

results = discover_by_category(
    "https://zeptonow.com/category/example",
    limit=100,
)
```

---

## 출력 필드

각 결과 레코드에는 다음 필드가 포함됩니다:

| Field | Description |
|-------|-------------|
| `url` | 상품 페이지 URL |
| `name` | 상품명 |
| `brand` | 브랜드 |
| `price` | 현재 가격 |
| `currency` | 통화 코드 |
| `unit_price` | 단위/중량당 가격 |
| `in_stock` | 재고 상태 |
| `category` | 상품 카테고리 |
| `sku` | SKU / 바코드 |
| `images` | 상품 이미지 URL |
| `description` | 상품 설명 |
| `timestamp` | 수집 타임스탬프 |

### 샘플 출력

```json
[
  {
    "url": "https://www.zeptonow.com/products/sample-product",
    "title": "Example Product Name",
    "brand": "Example Brand",
    "initial_price": 59.99,
    "final_price": 44.99,
    "currency": "USD",
    "discount": "25%",
    "in_stock": true,
    "rating": 4.5,
    "reviews_count": 1234,
    "images": ["https://zeptonow.com/images/product1.jpg"],
    "description": "Product description text...",
    "timestamp": "2025-01-15T10:30:00Z"
  }
]
```

---

## 고급 옵션

`trigger_collection()` 함수는 데이터 수집을 제어하기 위한 선택적 파라미터를 지원합니다:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | integer | - | 반환할 최대 레코드 수 |
| `include_errors` | boolean | `true` | 결과에 오류 리포트 포함 |
| `notify` | string (URL) | - | 스냅샷 준비 완료 시 호출할 webhook URL |
| `format` | string | `json` | 출력 형식: `json`, `csv` 또는 `ndjson` |

옵션 사용 예시:

```python
from price_tracker import trigger_collection, get_results

inputs = [{"url": "https://www.zeptonow.com/products/sample-product"}]
snapshot_id = trigger_collection(inputs, limit=200, notify="https://your-webhook.com/hook")
results = get_results(snapshot_id)
```

---

## 리소스

- 🌟 [Zepto Price Tracker - Bright Insights (Managed)](https://brightdata.co.kr/products/insights/price-tracker/zepto)
- 🏗️ [Zepto Scraper 구축하기](https://brightdata.co.kr/products/web-scraper/zepto)
- 📖 [Bright Data Web Scraper API 문서](https://docs.brightdata.co.kr/scraping-automation/web-scraper-api/overview)
- 🗄️ [Web Scrapers Control Panel](https://brightdata.co.kr/cp/scrapers)
- 🔑 [API token 발급 방법](https://docs.brightdata.co.kr/general/account/account-settings#api-token)
- 🌐 [Bright Data 홈페이지](https://brightdata.co.kr)

---

*[Bright Data](https://brightdata.co.kr)로 구축 - 업계를 선도하는 웹 데이터 플랫폼.*