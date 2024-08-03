# GPT4o mini OPENAI에서 파인튜닝하기.
* 2024년 9월 23일까지 1일당 200만개의 토큰만큼 무료로 파인튜닝이 가능함.

## Step0 데이터 세트 준비
 * 대화와 유사한 다양한 메모 대화 세트가 필요함. [예제](https://platform.openai.com/docs/api-reference/chat/create)

## Step 1 데이터 형식 확인.
 * 오류를 찾고 토큰 수 검토, 비용추정 [스크립트](https://cookbook.openai.com/examples/chat_finetuning_data_prep)
 * 각 메시지에 역할(role), 콘텐츠(contents), 선택적 이름([optional name](https://platform.openai.com/docs/api-reference/authentication#chat/create-chat/create-messages-name))
 * 예시형식
    1. 냉소적 답변 생성 챗봇
    ```
    {"messages": [{"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "What's the capital of France?"}, {"role": "assistant", "content": "Paris, as if everyone doesn't know that already."}]}
    {"messages": [{"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "Who wrote 'Romeo and Juliet'?"}, {"role": "assistant", "content": "Oh, just some guy named William Shakespeare. Ever heard of him?"}]}
    {"messages": [{"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "How far is the Moon from Earth?"}, {"role": "assistant", "content": "Around 384,400 kilometers. Give or take a few, like that really matters."}]}
    ```
    2. 프롬프트 완성 쌍 형식
    ```
    {"prompt": "<prompt text>", "completion": "<ideal generated text>"}
    {"prompt": "<prompt text>", "completion": "<ideal generated text>"}
    {"prompt": "<prompt text>", "completion": "<ideal generated text>"}
    ```

## Step 2 훈련 파일 업로드
 * 데이터 검증 완료시, 파일 API를 사용하여 파일을 업로드 하여 미세 조정 작업에 사용

    ```python
    from openai import OpenAI
    client = OpenAI()
    client.files.create(
    file=open("mydata.jsonl", "rb"),
    purpose="fine-tune"
    )
    ```
## Step 3 미세 조정된 모델 만들기
 1. [조정UI](https://platform.openai.com/finetune)를 통해 만들기
 2. OpenAI SDK 사용
    ```
    from openai import OpenAI
    client = OpenAI()
    client.fine_tuning.jobs.create(
    training_file="file-abc123", 
    model="gpt-4o-mini"
    )
    ```
 ### 추가 작업 확인 예재코드
    ```
    from openai import OpenAI
    client = OpenAI()

    # 파인 튜닝 작업 10개 목록
    client.fine_tuning.jobs.list(limit=10)

    # 파인 튜닝 상태 조회
    client.fine_tuning.jobs.retrieve("ftjob-abc123")

    # 작업 취소
    client.fine_tuning.jobs.cancel("ftjob-abc123")

    # 파인 튜닝 작업에서 이벤트 최대 10개 목록
    client.fine_tuning.jobs.list_events(fine_tuning_job_id="ftjob-abc123", limit=10)

    # 파인 튜닝된 모델 삭제 (모델이 생성된 조직의 소유자여야 함)
    client.models.delete("ft:gpt-3.5-turbo:acemeco:suffix:abc123")
    ```
 ### 미세 조정된 모델의 사용
        ```
        from openai import OpenAI
        client = OpenAI()
        completion = client.chat.completions.create(
        model="ft:gpt-4o-mini:my-org:custom_suffix:id",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
        ]
        )
        print(completion.choices[0].message)
        ```

## 체크포인트된 모델 사용
 * 최종 미세조정모델 외에도 각 훈련 에포크의 마지막에도 체크포인트를 생성한다고 합니다. 이를 사용하는 방법
        ```
        {
            "object": "fine_tuning.job.checkpoint",
            "id": "ftckpt_zc4Q7MP6XxulcVzj4MZdwsAB",
            "created_at": 1519129973,
            "fine_tuned_model_checkpoint": "ft:gpt-3.5-turbo-0125:my-org:custom-suffix:96olL566:ckpt-step-2000",
            "metrics": {
                "full_valid_loss": 0.134,
                "full_valid_mean_token_accuracy": 0.874
            },
            "fine_tuning_job_id": "ftjob-abc123",
            "step_number": 2000
        }
        ```
## 파인튜닝된 모델 분석
    1. 훈련 손실
    2. 훈련 토큰 정확도
    3. 유효한 손실
    4. 유효한 토큰 정확도
        ```
        {
            "object": "fine_tuning.job.event",
            "id": "ftevent-abc-123",
            "created_at": 1693582679,
            "level": "info",
            "message": "Step 300/300: training loss=0.15, validation loss=0.27, full validation loss=0.40",
            "data": {
                "step": 300,
                "train_loss": 0.14991648495197296,
                "valid_loss": 0.26569826706596045,
                "total_steps": 300,
                "full_valid_loss": 0.4032616495084362,
                "train_mean_token_accuracy": 0.9444444179534912,
                "valid_mean_token_accuracy": 0.9565217391304348,
                "full_valid_mean_token_accuracy": 0.9089635854341737
            },
            "type": "metrics"
        }
        ```

## 품질 향상을 위한 조치
    1. 데이터 양/질을 증가
    2. 하이퍼파라미터 지정(에포크 수 조정/학습률 배수)
        ```
        from openai import OpenAI
        client = OpenAI()

        client.fine_tuning.jobs.create(
        training_file="file-abc123", 
        model="gpt-4o-mini", 
        hyperparameters={
            "n_epochs":2
        }
        )
        ```