# Data

## 데이터 분석
- 데이터로 부터 유의미한 정보를 추출하여 결정 지원 과정

- 분석과정
  1. 목표 및 질문정의
  2. 데이터 수집
  3. 데이터 정제
  4. EDA (탐색적 데이터 분석) 
  5. 데이터 분석 및 모델링
  6. 결과 해석 및 시각화
  7. 스토리텔링

- 중요성
 * 경쟁 우위 확보
 * 의사결정 개선
 * 효율성 증가
 * 고객 이해 및 서비스 개선

### 데이터의 종류와 속성
- 정량적 데이터(Quantitative Data) : 수치로 표현되는 데이터
- 정성적 데이터(Qualitative Data) : 문자, 동영상 등으로 분류되는 데이터
- 수치형 데이터(Numerial Data) : 연속형(온도,무게) 및 이산형 데이터
- 범주형 데이터 (Categorical Data) : 범주화된 제한된 범위의 값을 가짐

### EDA [Pandas, NumPy, Matplotlib, Seaborn]
시각화와 요약을 통해 중요 특성과 패턴 발견 과정
- 데이터 분포의 이해
- 이상치 탐지
- 변수 간 관계 파악
- 데이터 구조 이해
- 가설 생성

### 상관관계 및 인과관계
- 상관관계(Correlation) : 두 변수간의 연관성을 수치적으로 나타내는 지표
- 인과관계(Causuality) : 한 변수(원인)의 변화가 다른 변수(결과)의 변화를 유발

### 가설 검정과 A/B테스트
- 가설 검정 : 표본 데이터를 사용해 모집단에 대한 통계적 가설의 타당성 판단
- A/B 테스트 : 두 가지 이상의 버전을 테스트하여 어느 것이 더 효과적인지 결정하는 방법

### 시계열 데이터
시간의 순서대로 정렬된 데이터 포인트의 연속

- 특성
    * 추세 (Trend) : 장기적인 데이터 증감 경향
    * 계절성 (Seasonality) : 특정 시간 패턴이 반복 [월별, 주별, 일별 패턴]
    * 주기성 (Cyclicality) : 불규칙적인 간격으로 반복되는 변동
    * 잡음 (Noise) : 데이터에 포함된 불규칙한 변동

- 분석방법
    * 시계열 분해 :  
    [가법 모형] : 개별 요인의 효과를 구분하고 함께 더하여 데이터를 모형화하는 데이터 모형
    [승법 모형] : 데이터가 증가하면 계절 패턴도 증가한다고 가정하는 모형

    * 통계적 방법
    [이동 평균 (Moving Average)] : 데이터의 단기 변동을 평활화
    [지수 평활(Exponential Smoothing)] : 최근 관측값에 더 큰 가중치를 두는 방법

    * 시계열 예측:
    [ARIMA 모델] : 자기회귀 통합 이동평균 모델로 시계열 데이터 예측
    결측치 해결 : 보간법(interpolation), 평균으로 대체하여 처리
    이상치 해결 : Z-Score, IQR(Interquartile Range) 

### 다변량 분석
여러 현상이나 사건에 대한 측정치를 개별적으로 분석하지 않고 동시에 한번에 분석하는 통계적 기법

- 두 개 이상의 변수를 동시에 분석하는 기법으로, 변수들 간의 관계를 파악하고, 패턴을 예측
- 단변량 분석에서 간과할 수 있는 변수들 간의 상호작용과 복잡한 관계를 포착 가능
    * 상관분석 : 변수간 관계의 방향, 강도를 측정
    [피어슨 상관계수(Pearson Correlation)] : 두 변수 간의 선형 관계의 강도와 방향을 측정하는 통계적 방법.연속적, 정규 분포에 적합
    [스피어만 상관계수(Spearman Correlation)] : 두 변수의 순위에 기반하여 관계를 측정하는 비모수적 방법. 순위형, 정규분포를 따르지 않을 때 적합
    * 주성분 분석(PCA - Principal Component Analysis) : 고차원 데이터의 차원을 축소하여 중요한 특성 추출
    * 요인 분석 : 변수들 사이의 관계를 분석하여 몇 가지 잠재적 요인 탐색

### 실시간 데이터 분석

### 데이터 기반 의사결정
주관성을 최소화 한 데이터 기반 최적의 결과를 도출

## 데이터 시각화
데이터를 그래픽 요소료 변환하여 시각적으로 표현하는 과정

### 기본 차트 유형 및 사용법
* 막대그래프 : 범주형 데이터의 빈도나 값
- [각 달별 판매량 비교]
```python
import matplotlib.pyplot as plt

# 데이터
categories = ['A', 'B', 'C']
values = [10, 15, 7]

# 막대그래프
plt.bar(categories, values)
plt.show()
```

* 히스토그램 : 연속형 데이터의 분포
```python
import matplotlib.pyplot as plt
import numpy as np

# 데이터
data = np.random.randn(1000)

# 히스토그램
plt.hist(data, bins=30)
plt.show()
```

* 선 그래프 : 시간에 따른 데이터 변화
[주가 변동]
```python
import matplotlib.pyplot as plt

# 데이터
x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 7, 11]

# 선그래프
plt.plot(x, y)
plt.show()
```

* 파이차트 : 전체에서 각 부분의 비율을 시각화하는데 사용
[시장 점유율]
```python
import matplotlib.pyplot as plt

# 데이터
sizes = [15, 30, 45, 10]
labels = ['A', 'B', 'C', 'D']

# 파이차트
plt.pie(sizes, labels=labels)
plt.show()
```

* 산점도 : 두 변수간의 관계를 시각화
[키와 몸무게 간의 상관관계]
```python
import matplotlib.pyplot as plt

# 데이터
x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 7, 11]

# 산점도
plt.scatter(x, y)
plt.show()
```

* 박스플롯 : 데이터의 분포와 이상치를 시각화
[여러 실험군의 반응 시간 비교]
```python
import matplotlib.pyplot as plt
import numpy as np

# 데이터
data = [np.random.randn(100) for _ in range(4)]

# 박스플롯
plt.boxplot(data)
plt.show()
```