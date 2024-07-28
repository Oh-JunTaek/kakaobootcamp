# 용어 정리

## 데이터 수집 방법

### BeautifulSoap
웹 스크래핑 라이브러리(HTML/XML에 강함)
```python
from bs4 import BeautifulSoup

# HTML 문서 로드
html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

# BeautifulSoup 객체 생성
soup = BeautifulSoup(html_doc, 'html.parser')

# 데이터 추출
print(soup.title.string)  # 'The Dormouse's story'
print(soup.p.text)  # 'The Dormouse's story'
print(soup.find_all('a'))  # 모든 <a> 태그 찾기
```

* 강점
1. 간단한 API
2. 다양한 파서 지원
3. 유연성 - selector를 제공하여 원하는 데이터를 쉽게 찾음. 태그, 클래스, ID, 속성 등을 조합하여 선택
4. 오류 처리

* 단점
1. 속도저하 - 다소 느린편에 속해 대량데이터에 성능저하발생
2. 메모리사용량 - HTML/XML 문서를 트리 구조로 표현하므로 메모리 사용량이 많아 대용량 문서 처리시 메모리 부족
3. 복잡한 문서 처리 - 단순한 문서에는 강하지만 복잡한 문서에는 적합하지 않음
4. 동적 컨텐츠의 처리가 어려움. - js로 생성되는 동적 컨텐츠에는 약하기에 Selenium과 같은 도구를 사용

### Scrapy
오픈 소스 웹 크롤링 및 스크래핑 프레임워크
* 강점
1. 고성능 - 비동기 I/O를 사용하여 빠르고 효율적인 크롤링
2. 유연성 - 다양한 확장 기능과 사용자 정의 옵션을 통해 다양한 크롤링 요구사항에 맞출 수 있음.
3. 커뮤니티 - 풍부한 문서, 튜토리얼을 통해 쉽게 학습 가능
4. 데이터 수집 파이프라인 - 데이터 수집, 처리, 저장을 위한 파이프라인을 쉽게 구성

* 단점
1. 학습곡선 - 비동기 I/O와 프레임 워크 구조에 익숙해지는데 시간이 소요됨
2. 간단한 작업에는 과도할 수 있음
3. 동적 콘텐츠 처리 어려움

* 사용방법
  실습내용 참고

###requests
HTTP 클라이언트 라이브러리
* 강점
1. 간단하고 직관적
2. 다양한 HTTP기능 지원
3. 높은 안정성
4. 활발한 커뮤니티

* 단점
1. 속도저하 : 내부적으로 urllib3 라이브러리 사용으로 대량의 요청에 성능이 저하 됨
2. 동적 콘텐츠 처리가 어려움

* 사용방법
1. 라이브러리 설치
```bash
pip install requests
```

2. GET 요청보내기 
```python
import requests

response = requests.get('https://www.example.com')
print(response.status_code)  # 200
print(response.text)  # HTML
```

3. POST요청 보내기
```python
import requests

data = {'key1': 'value1', 'key2': 'value2'}
response = requests.post('https://www.example.com/api', data=data)
print(response.status_code)  # 200
print(response.json())  # J
```

4. 세션관리
```python
import requests

session = requests.Session()
session.auth = ('username', 'password')
response = session.get('https://www.example.com/protected')
print(response.status_code)
```

### Selenium
웹 애플리케이션의 테스트 자동화를 위한 강력한 도구(브라우저, 프로그래밍언어, 웹앱 기능테스트, 크롤링, 스크래핑)

* 강점
1. 브라우저 자동화 - 다양한 웹브라우저를 자동으로 제어
2. 다양한 언어와 브라우저 지원
3. 동적 컨텐츠 처리 가능
4. 확장성 및 유연성 - WebDriver API

* 단점
1. 초기설정 및 설치의 복잡함
2. 실제 브라우저 구동으로 인한 높은 자원소모와 속도가 느림.
3. 유지보수 - 잦은 스크립트 업데이트

* 사용방법
1. 설치
```bash
pip install selenium
```

2. 브라우저 자동화 예제
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 웹 드라이버 경로 설정
driver = webdriver.Chrome(executable_path='/path/to/chromedriver')

# 웹 페이지 열기
driver.get('https://www.example.com')

# 요소 찾기 및 상호작용
search_box = driver.find_element(By.NAME, 'q')
search_box.send_keys('Selenium')
search_box.send_keys(Keys.RETURN)

# 결과 출력
print(driver.title)

# 브라우저 닫기
driver.quit()
```

3. 동적 컨텐츠 처리
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(executable_path='/path/to/chromedriver')
driver.get('https://www.example.com')

try:
    # 특정 요소가 로드될 때까지 대기
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'dynamic-element-id'))
    )
    print(element.text)
finally:
    driver.quit()
```