# crawler.py
# 목적: 여러 페이지의 책 정보를 수집해서 books.csv로 저장
#
# 2단계와 달라진 점
#   1) 같은 작업을 함수(fetch_books)로 묶어서 페이지마다 반복 실행
#   2) 결과를 화면에 출력하는 대신 CSV 파일로 저장

import csv          # CSV 파일 저장용
import time         # 요청 사이에 쉬기 위한 용도
import requests     # HTTP 요청
from bs4 import BeautifulSoup  # HTML 파싱

# 페이지 주소 틀. {} 자리에 페이지 번호가 들어갑니다.
# 사이트 아래쪽 "next" 버튼을 눌러 보면 주소가
# page-1.html, page-2.html, page-3.html ... 로 바뀌는 것을 볼 수 있습니다.
BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

# 요청 헤더: "브라우저에서 보낸 요청입니다"라고 알려 주는 정보 (학습용 기본값)
HEADERS = {"User-Agent": "Mozilla/5.0"}


def fetch_books(page_num):
    """한 페이지의 책 목록을 dict 리스트로 반환합니다.
    페이지가 없으면(404) None을 반환합니다."""

    url = BASE_URL.format(page_num)           # 예: page_num=2 → .../page-2.html
    res = requests.get(url, headers=HEADERS, timeout=10)

    if res.status_code == 404:                # 더 이상 페이지가 없을 때
        return None
    res.raise_for_status()                    # 그 밖의 오류는 예외로 처리

    res.encoding = "utf-8"                    # "£"가 "Â£"로 깨지지 않게 지정
    soup = BeautifulSoup(res.text, "html.parser")

    books = []
    # 페이지 안의 모든 책 카드를 순회
    for art in soup.select("article.product_pod"):
        # 책 한 권 = dict 하나 (열 이름: 값)
        books.append({
            # 책 제목: h3 > a 태그의 title 속성
            "title": art.h3.a["title"],
            # 가격: class가 price_color인 p 태그의 글자
            "price": art.select_one("p.price_color").text,
            # 별점: class 목록 ["star-rating", "Three"]의 두 번째 값
            "rating": art.select_one("p.star-rating")["class"][1],
        })
    return books


def main():
    all_books = []                            # 전체 결과를 담을 리스트

    # 오늘은 3페이지만 수집 (range(1, 4) → 1, 2, 3)
    for page in range(1, 4):
        books = fetch_books(page)
        if books is None:                     # 페이지가 없으면 중단
            break

        all_books.extend(books)               # 이번 페이지 결과를 전체에 합치기
        print(f"{page}페이지 완료: {len(books)}권")
        time.sleep(1)                         # 서버 부담을 줄이기 위해 1초 대기

    print("총", len(all_books), "권 수집")
    for b in all_books[:5]:                   # 앞부분 5개만 미리보기
        print(b)

    # CSV로 저장
    # encoding="utf-8-sig": 엑셀에서 열어도 글자가 깨지지 않게 하는 설정
    # newline="": 줄 사이에 빈 줄이 끼지 않게 하는 설정
    with open("books.csv", "w", newline="", encoding="utf-8-sig") as f:
        # 열 이름 순서 지정
        writer = csv.DictWriter(f, fieldnames=["title", "price", "rating"])
        writer.writeheader()                  # 첫 줄에 열 이름 쓰기
        writer.writerows(all_books)           # 모든 행 쓰기
    print("books.csv 저장 완료")


# 이 파일을 직접 실행했을 때만 main() 호출
if __name__ == "__main__":
    main()
