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

# 인코딩 지정
# requests가 인코딩을 잘못 추측하면 "£"가 "Â£"처럼 깨집니다.
# 이 사이트는 UTF-8이므로 직접 알려 줍니다. (이 줄을 지우고 실행해서 비교해 보세요)
res.encoding = "utf-8"

# 2) HTML 파싱
# res.text는 받아온 HTML 원문 문자열이고,
# BeautifulSoup은 이를 탐색하기 쉬운 객체로 바꿔 줍니다.
soup = BeautifulSoup(res.text, "html.parser")

# 3) 페이지 제목 추출
# .text는 태그 안의 글자만 꺼내고, .strip()은 앞뒤 공백/줄바꿈을 지웁니다.
title = soup.title.text.strip()
print("페이지 제목:", title)

# 4) 책 목록 추출
# 각 책은 <article class="product_pod"> 태그 안에 있습니다.
books = soup.select("article.product_pod")  # CSS 선택자로 모두 찾기 (리스트 반환)
print("책 수:", len(books))
print("-" * 50)

# enumerate(books, 1): 번호(1부터)와 책을 함께 꺼냅니다.
for i, book in enumerate(books, 1):
    # 책 제목은 h3 아래 a 태그의 title 속성에 들어 있습니다.
    # (화면 글자는 "A Light in the ..."처럼 잘려 있어서 속성 값을 씁니다)
    name = book.h3.a["title"]

    # 가격은 class가 price_color인 p 태그의 글자입니다.
    # select_one()은 조건에 맞는 첫 번째 태그 하나만 반환합니다.
    price = book.select_one("p.price_color").text

    print(f"{i:2}. {name} / {price}")
