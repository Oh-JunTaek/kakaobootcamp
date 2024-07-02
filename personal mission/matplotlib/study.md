# matplotlib를 사용하여 데이터 시각화 실습

## 결측값이상치 처리하기.

### 특징
* 결측값을 평균, 중앙값으로 대체하거나 제거할 수 있음.
* 이상치를 IQR, Z-Score등의 방법을 사용하여 식별/제거할 수 있음.

### 코드예시
```python
import pandas as pd

# 데이터 불러오기
df = pd.read_csv('data.csv')

# 결측값 확인
print(df.isnull().sum())

# 결측값 처리 (평균으로 대체)
df.fillna(df.mean(), inplace=True)

# 이상치 확인 (IQR 방법)
Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)
IQR = Q3 - Q1
outliers = df[((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).any(axis=1)]

# 이상치 제거
df = df[~((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).any(axis=1)]
```


## 막대그래프 

### 특징
* 범주형 데이터를 시각화 할 때 유용함
* 각 범주에 대한 값을 쉽게 비교 가능

### 코드예시
```python
import matplotlib.pyplot as plt

# 데이터 준비
categories = ['A', 'B', 'C']
values = [10, 20, 15]

# 막대그래프 생성
plt.bar(categories, values)

# 그래프 표시
plt.show()
```

## 선그래프

### 특징
* 시간에 따른 데이터 변화나 추세를 시각화할 때 유용함
* 여러 데이터를 한 그래프에 표시하여 비교할 수 있음

### 코드예시
```python
# 데이터 준비
x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 7, 11]

# 선그래프 생성
plt.plot(x, y)

# 그래프 표시
plt.show()
```

## 산점도

### 특징
* 두 변수간의 관계를 시각화 할 때 유용함
* 데이터의 분포와 클러스터를 쉽게 식별

### 코드예시
```python
# 데이터 준비
x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 7, 11]

# 산점도 생성
plt.scatter(x, y)

# 그래프 표시
plt.show()
```

## 히스토그램

### 특징
* data의 분포를 시각화 할때 유용함.
* 데이터의 빈도와 패턴을 쉽게 파악

### 코드예시
```python
# 데이터 준비
data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]

# 히스토그램 생성
plt.hist(data, bins=4)

# 그래프 표시
plt.show()
```

## 이미지로 저장
```python
# 그래프 이미지 파일로 저장
plt.savefig('line_graph.png')

# 그래프 표시
plt.show()
```