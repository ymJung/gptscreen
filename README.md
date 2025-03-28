# GPT Screen

음성 인식을 통해 GPT와 대화할 수 있는 데스크톱 애플리케이션입니다.

## 주요 기능

- 음성 인식을 통한 GPT와의 대화
- 시작 키워드("어이")와 끝 키워드("오버")를 통한 자연스러운 대화
- 5초 이상 침묵 시 자동 질문 처리
- 실시간 상태 표시 (질문 대기중/생성중)

## 설치 방법

1. 필요한 패키지 설치:
```bash
pip install speech_recognition openai tkinter
```

2. `config.cfg.example`을 `config.cfg`로 복사하고 OpenAI API 키 설정:
```ini
[openai]
TOKEN=your-api-key-here
```

## 사용 방법

1. 프로그램 실행:
```bash
python main.py
```

2. 음성 명령 사용:
   - "어이"로 시작: 질문 모드 시작 (빨간색으로 "질문 대기중..." 표시)
   - 질문 말하기
   - "오버"로 끝내기 또는 5초 동안 침묵 (자동으로 "생성중..." 표시)

## 상태 표시

- 검은색 "마이크 대기 중...": 평상시 상태
- 빨간색 "질문 대기중...": 질문을 받을 준비가 된 상태
- 빨간색 "생성중...": GPT가 답변을 생성하는 상태

## 주의사항

- 마이크가 정상적으로 연결되어 있는지 확인하세요
- 인터넷 연결이 필요합니다
- OpenAI API 키가 올바르게 설정되어 있어야 합니다

## 문제 해결

- 음성이 인식되지 않을 경우: 마이크 연결 및 권한 설정 확인
- API 오류 발생 시: OpenAI API 키 확인
- 프로그램이 응답하지 않을 경우: 프로그램 재시작