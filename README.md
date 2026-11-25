# 파이썬 크롤링 2시간 학습

연습용 공개 사이트 [books.toscrape.com](https://books.toscrape.com/)에서 책 정보를 수집하며 크롤링의 기본을 익히는 학습 기록입니다.

**학습 페이지:** https://tosolvetheproblem.github.io/crawling_practice/

크롤링은 세 단계로 이루어집니다.

```
① 가져오기 (requests)  →  ② 찾기 (BeautifulSoup)  →  ③ 저장하기 (csv)
```

## 파일

| 파일 | 설명 |
|---|---|
| [python_crawling_study.md](python_crawling_study.md) | 2시간 학습 계획 |
| [step1_structure.py](step1_structure.py) | 1단계: robots.txt와 HTML 구조 확인 |
| [first_crawler.py](first_crawler.py) | 2단계: 1페이지에서 책 20권의 제목과 가격 출력 |
| [crawler.py](crawler.py) | 3단계: 3페이지 60권을 books.csv로 저장 |
| [books.csv](books.csv) | 수집 결과 |
| [docs/index.html](docs/index.html) | 학습 페이지 (GitHub Pages) |
| [WORK_LOG.md](WORK_LOG.md) | 작업 로그 |

## 실행

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install requests beautifulsoup4 pandas
python first_crawler.py
python crawler.py
```
