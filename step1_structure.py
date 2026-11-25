# step1_structure.py
# 목적: 크롤링 전에 (1) robots.txt로 수집 허용 여부를 확인하고
#       (2) 책 한 권의 HTML 구조를 눈으로 확인한다.

import requests                   # HTTP 요청을 보내는 라이브러리
from bs4 import BeautifulSoup     # HTML을 분석(파싱)하는 라이브러리

URL = "https://books.toscrape.com/"

# 1) robots.txt 확인
#    사이트가 자동 수집을 어디까지 허용하는지 적어 둔 파일입니다.
#    404가 나오면 별도의 제한 규칙이 없다는 뜻입니다.
robots = requests.get(URL + "robots.txt", timeout=10)
print("[robots.txt] 상태 코드:", robots.status_code)
if robots.status_code == 200:
    print(robots.text)

# 2) 메인 페이지 HTML 가져오기
res = requests.get(URL, timeout=10)
res.raise_for_status()            # 오류 응답이면 여기서 멈춤
soup = BeautifulSoup(res.text, "html.parser")

# 3) 책 카드(article.product_pod)가 몇 개 있는지 확인
books = soup.select("article.product_pod")
print("\n이 페이지의 책 수:", len(books))   # 한 페이지에 20권이면 정상

# 4) 첫 번째 책의 HTML을 보기 좋게 출력
#    prettify()는 들여쓰기를 넣어 태그 구조를 읽기 쉽게 만들어 줍니다.
#    F12에서 본 구조와 같은지 비교해 보세요.
print("\n[첫 번째 책 HTML 구조]")
print(books[0].prettify())
