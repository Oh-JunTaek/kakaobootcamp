# kakaobootcamp
카카오 부트캠프 교육과정 
# 7월 1주
## 강의/교육

## 학습/공부

## 실습
### 개발환경 세팅
* Python 개발환경 - 사전에 완료하였음.(파이썬 설치, 필요한 라이브러리 설치, 아나콘다 설치)* github - 미흡하나 운영중
### 사전평가
### 크롤링
* scrapy를 사용해서 한국위키피디아 또는 원하는 웹사이트 크롤링해보기
  1. 위키피디아 페이지 중 https://ko.wikipedia.org/wiki/%EC%B9%B4%EC%B9%B4%EC%98%A4_(%EA%B8%B0%EC%97%85) 페이지를 크롤링 하기로 목표 설정
  2. 설치 
```bash
pip install scrapy
```
  3. 파일명을 설정하여 프로젝트 시작
```bash     
scrapy startproject wikikakao 
```
  4. 터미널 작업 폴더 이동 
```bash
cd wikikakao
```
  5. 스파이더 파일 생성 
```bash
scrapy genspider kakao_spider ko.wikipedia.org
```
  6. 스파이더 파일에서 긁어올 내용을 포함하여 코드를 수정
```python
import scrapy
class KakaoSpider(scrapy.Spider):
    name = 'kakao_spider'
    allowed_domains = ['ko.wikipedia.org']
    start_urls = ['https://ko.wikipedia.org/wiki/%EC%B9%B4%EC%B9%B4%EC%98%A4_(%EA%B8%B0%EC%97%85)']

    def parse(self, response):
        title = response.xpath('//h1/text()').get()
        paragraphs = response.xpath('//p//text()').getall()

        yield {
            'title': title,
            'paragraphs': paragraphs,
        }
```
  7. 크롤링 실행 후 json파일로 저장 
```bash
scrapy crawl kakao_spider -o output.json
```
