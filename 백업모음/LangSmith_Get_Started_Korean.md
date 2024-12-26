
# LangSmith 시작하기

LangSmith는 **프로덕션급 LLM 애플리케이션**을 구축하는 플랫폼입니다. 이 도구는 애플리케이션을 **모니터링**하고 **평가**하여 빠르고 신뢰성 있는 배포를 가능하게 합니다. LangChain과 함께 사용하지 않아도 독립적으로 작동할 수 있습니다!

## 1. LangSmith 설치

Python 환경에서 LangSmith를 설치하려면 다음 명령어를 사용합니다:

```bash
pip install -U langsmith
```

## 2. API 키 생성

LangSmith를 사용하려면 API 키가 필요합니다. **Settings 페이지**로 이동하여 **API Key 생성(Create API Key)** 버튼을 클릭하세요.

## 3. 환경 설정

환경 변수를 설정하여 LangSmith를 사용 준비합니다:

```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export OPENAI_API_KEY=<your-openai-api-key>  # OpenAI API를 사용할 경우에만 필요
```

## 4. 첫 추적 로그 남기기

LangSmith SDK를 직접 사용할 필요 없이, **LangChain 사용 시 자동으로 추적**이 가능합니다. 아래는 Python 예제 코드입니다.

```python
import openai
from langsmith.wrappers import wrap_openai
from langsmith import traceable

# LLM 호출을 자동으로 추적
client = wrap_openai(openai.Client())

@traceable  # 이 함수는 자동으로 추적됨
def pipeline(user_input: str):
    result = client.chat.completions.create(
        messages=[{"role": "user", "content": user_input}],
        model="gpt-3.5-turbo"
    )
    return result.choices[0].message.content

pipeline("Hello, world!")  # "Hello there! How can I assist you today?" 출력
```

## 5. 첫 번째 평가 수행

LangSmith는 **자동 평가 도구**를 제공하여, 정확도나 일치도와 같은 평가를 수행할 수 있습니다. 예를 들어, OpenAI의 결과를 정확도 기반으로 평가하는 코드입니다:

```python
from langsmith import Client
from langsmith.evaluation import evaluate

client = Client()

# 데이터셋 정의
dataset_name = "Sample Dataset"
dataset = client.create_dataset(dataset_name, description="샘플 데이터셋입니다.")
client.create_examples(
    inputs=[{"postfix": "to LangSmith"}, {"postfix": "to Evaluations in LangSmith"}],
    outputs=[{"output": "Welcome to LangSmith"}, {"output": "Welcome to Evaluations in LangSmith"}],
    dataset_id=dataset.id,
)

# 평가 함수 정의
def exact_match(run, example):
    return {"score": run.outputs["output"] == example.outputs["output"]}

# 평가 수행
experiment_results = evaluate(
    lambda input: "Welcome " + input['postfix'],  # 평가 대상 시스템
    data=dataset_name,  # 평가할 데이터셋
    evaluators=[exact_match],  # 평가 기준
    experiment_prefix="sample-experiment",  # 실험 이름
    metadata={"version": "1.0.0", "revision_id": "beta"},
)
```

---

## 핵심 개념 설명

### 1. **LLM(대규모 언어 모델)**
LLM은 대규모 데이터셋으로 학습된 **자연어 처리 모델**로, 사람의 언어를 이해하고 생성할 수 있습니다. 대표적인 예로는 **GPT**와 같은 모델이 있으며, 이들은 텍스트를 생성하고, 번역하며, 질문에 답할 수 있습니다.

### 2. **RAG(Retrieval-Augmented Generation)**
RAG는 **문서 기반 정보 검색**과 **언어 모델 생성 능력**을 결합한 방식입니다. 사용자가 질문을 했을 때, 모델은 검색된 문서에서 관련 정보를 추출한 후, 그 정보를 기반으로 응답을 생성합니다.

### 3. **추적(Tracing)**
LangSmith의 **추적 기능**은 LLM 애플리케이션에서 발생하는 각 단계를 기록하여 **오류 발생 지점**이나 **병목 현상**을 확인할 수 있게 합니다. 이를 통해 애플리케이션의 성능을 실시간으로 모니터링하고 개선할 수 있습니다.

### 4. **평가(Evaluation)**
LangSmith는 애플리케이션의 성능을 **자동 평가**할 수 있는 도구를 제공합니다. 정확도, 일치도, 효율성 등을 평가하여, 모델의 응답 품질을 지속적으로 향상시킬 수 있습니다.
