# 파이썬 크롤링 학습 (2시간 과정)

연습 대상: `https://books.toscrape.com/` (스크래핑 연습용 공개 사이트)

> 네이버 부동산은 robots.txt에서 `Disallow: /`로 자동 수집을 막고 있으므로 학습 대상에서 제외합니다.

## 전체 학습 순서

| 시간 | 단계 | 내용 | 시간 배분 |
|---|---|---|---|
| 오늘 밤 | 1단계 | 환경 준비와 사이트 구조 보기 | 10분 |
| 오늘 밤 | 2단계 | 페이지 1개에서 데이터 뽑기 | 15분 |
| 오늘 밤 | 3단계 | 여러 페이지 수집 후 CSV 저장 | 35분 |
| 내일 오전 | 4단계 | pandas로 데이터 정제 | 30분 |
| 내일 오전 | 5단계 | 결과 확인과 정리 | 30분 |

---

## 1단계: 환경 준비와 구조 보기 (10분)

```bash
pip install requests beautifulsoup4 pandas
```

브라우저에서 `https://books.toscrape.com/`을 열고 **F12 → 요소 선택 도구**로 책 하나를 클릭해 보세요.

- 책 한 권이 `<article class="product_pod">` 태그로 감싸져 있는지 확인합니다.
- 이 구조를 알고 있으면 크롤링 코드를 이해하기 쉽습니다.

---

## 2단계: 페이지 하나에서 데이터 뽑기 (15분)

```python
# first_crawler.py
# 목적: 웹 페이지 하나를 가져와 제목과 책 목록을 출력하는 기초 예제

import requests                   # HTTP 요청을 보내는 라이브러리
from bs4 import BeautifulSoup     # HTML을 분석(파싱)하는 라이브러리

# 연습용 사이트 주소
URL = "https://books.toscrape.com/"

# 1) 웹 페이지 요청
res = requests.get(URL, timeout=10)  # 10초 안에 응답이 없으면 실패 처리
res.raise_for_status()               # 4xx, 5xx 오류면 예외 발생

print("상태 코드:", res.status_code)  # 200이면 정상

# 2) HTML 파싱
# res.text는 받아온 HTML 원문 문자열이고,
# BeautifulSoup은 이를 탐색하기 쉬운 객체로 바꿔 줍니다.
soup = BeautifulSoup(res.text, "html.parser")

# 3) 페이지 제목 추출
title = soup.title.text              # <title> 태그의 글자
print("페이지 제목:", title)

# 4) 책 목록 추출
# 각 책은 <article class="product_pod"> 태그 안에 있습니다.
books = soup.select("article.product_pod")  # CSS 선택자로 모두 찾기

for book in books:
    # 책 제목은 h3 아래 a 태그의 title 속성에 들어 있습니다.
    name = book.h3.a["title"]

    # 가격은 class가 price_color인 p 태그의 글자입니다.
    price = book.select_one("p.price_color").text

    print(name, "/", price)
```

**실행:** `python first_crawler.py`

핵심 개념
- `requests.get()`: 웹 페이지 HTML을 가져온다.
- `BeautifulSoup`: HTML을 탐색 가능한 구조로 바꾼다.
- `select()`: CSS 선택자로 원하는 태그를 찾는다.

---

## 3단계: 여러 페이지 수집 후 CSV 저장 (35분)

```python
# crawler.py
# 목적: 여러 페이지의 책 정보를 수집해서 books.csv로 저장

import csv          # CSV 파일 저장용
import time         # 요청 사이에 쉬기 위한 용도
import requests     # HTTP 요청
from bs4 import BeautifulSoup  # HTML 파싱

# 페이지 주소 틀. {} 자리에 페이지 번호가 들어갑니다.
BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

# 요청 헤더 (학습용 기본값)
HEADERS = {"User-Agent": "Mozilla/5.0"}


def fetch_books(page_num):
    """한 페이지의 책 목록을 dict 리스트로 반환합니다.
    페이지가 없으면(404) None을 반환합니다."""

    url = BASE_URL.format(page_num)           # 실제 주소 만들기
    res = requests.get(url, headers=HEADERS, timeout=10)

    if res.status_code == 404:                # 더 이상 페이지가 없을 때
        return None
    res.raise_for_status()                    # 그 밖의 오류는 예외로 처리

    soup = BeautifulSoup(res.text, "html.parser")

    books = []
    # 페이지 안의 모든 책 카드를 순회
    for art in soup.select("article.product_pod"):
        books.append({
            # 책 제목: h3 > a 태그의 title 속성
            "title": art.h3.a["title"],
            # 가격: class가 price_color인 p 태그의 글자
            "price": art.select_one("p.price_color").text,
            # 별점: star-rating 클래스 안의 두 번째 값 (예: "Three")
            "rating": art.select_one("p.star-rating")["class"][1],
        })
    return books


def main():
    all_books = []                            # 전체 결과를 담을 리스트

    # 오늘은 3페이지만 수집 (나중에 범위를 늘리면 됩니다)
    for page in range(1, 4):
        books = fetch_books(page)
        if books is None:                     # 페이지가 없으면 중단
            break

        all_books.extend(books)               # 결과 합치기
        print(f"{page}페이지 완료: {len(books)}권")
        time.sleep(1)                         # 서버 부담을 줄이기 위해 1초 대기

    print("총", len(all_books), "권 수집")
    for b in all_books[:5]:                   # 앞부분 5개만 미리보기
        print(b)

    # CSV로 저장
    with open("books.csv", "w", newline="", encoding="utf-8-sig") as f:
        # 열 이름 순서 지정
        writer = csv.DictWriter(f, fieldnames=["title", "price", "rating"])
        writer.writeheader()                  # 첫 줄에 열 이름 쓰기
        writer.writerows(all_books)           # 모든 행 쓰기
    print("books.csv 저장 완료")


# 이 파일을 직접 실행했을 때만 main() 호출
if __name__ == "__main__":
    main()
```

**실행:** `python crawler.py`

**오늘 밤 완료 기준:** `books.csv` 파일이 생기고, 총 60권이 출력되면 성공입니다.

---

## 4단계: pandas로 정제 (내일 오전 30분)

```python
# clean.py
# 목적: 수집한 CSV에서 가격을 숫자로 바꾸고 기본 통계를 확인

import pandas as pd  # 표 형태 데이터를 다루는 라이브러리

# CSV 읽기
df = pd.read_csv("books.csv")

# 가격 문자열("£51.77", 일부는 "Â£51.77")에서 기호를 지우고 숫자(float)로 변환
df["price_num"] = (
    df["price"]
    .str.replace("Â", "", regex=False)   # 깨진 문자 제거
    .str.replace("£", "", regex=False)   # 파운드 기호 제거
    .astype(float)                       # 숫자 타입으로 변환
)

# 별점 글자("Three")를 숫자(3)로 변환
rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
df["rating_num"] = df["rating"].map(rating_map)

# 중복 행 제거
df = df.drop_duplicates()

# 기본 통계 출력 (평균, 최소, 최대 등)
print(df[["price_num", "rating_num"]].describe())

# 가격이 가장 비싼 책 5권
print(df.sort_values("price_num", ascending=False).head(5))

# 정제된 데이터 저장
df.to_csv("books_clean.csv", index=False, encoding="utf-8-sig")
print("books_clean.csv 저장 완료")
```

---

## 5단계: 결과 확인과 정리 (내일 오전 30분)

1. `books_clean.csv`를 엑셀로 열어 확인합니다.
2. 별점별 평균 가격을 구해 봅니다.

```python
# 별점별 평균 가격 (df는 4단계 코드에서 만든 DataFrame)
print(df.groupby("rating_num")["price_num"].mean())
```

3. 오류가 생기면 **오류 메시지 전체**를 복사해서 질문합니다.

---

## 체크리스트

- [ ] 1단계: 패키지 설치, 사이트 구조 확인
- [ ] 2단계: `first_crawler.py` 실행 성공
- [ ] 3단계: `books.csv` 생성, 60권 수집
- [ ] 4단계: `books_clean.csv` 생성, 가격 숫자 변환 완료
- [ ] 5단계: 별점별 평균 가격 확인

## 주의사항

- 요청 사이에 `time.sleep()`으로 간격을 둡니다.
- 대상 사이트의 robots.txt와 이용약관을 먼저 확인합니다.
- 차단 응답(403, 429)이 나오면 즉시 중단합니다.
