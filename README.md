# GPT TO SCREEN
- PC의 마이크를 활용, 상시로 GPT에 질문을 하고, 답은 화면에서 확인한다.

# flow-chart
1. 마이크를 활용하여 사용자 질문을 받음
2. GPT에 질문을 하고, 답은 화면에서 확인
    2.1 답이 나오는동안 마이크는 멈춰있게한다.
    2.2 질문이 다되면 약속된 단어를 말하면 답장 (ex. 왜그럴까?)
    2.3 질문은 약속된 단어로 시작한다 (ex.궁금한게 있는데)

``` mermaid
flowchart TD
    Start([시작]) --> Listen[마이크 대기]
    Listen --> CheckKeyword{시작 키워드 확인<br/>'궁금한게 있는데'}
    CheckKeyword -->|No| Listen
    CheckKeyword -->|Yes| Record[음성 녹음]
    Record --> CheckEnd{종료 키워드 확인<br/>'왜그럴까?'}
    CheckEnd -->|No| Record
    CheckEnd -->|Yes| Process[GPT에 질문 전송]
    Process --> DisplayResponse[화면에 답변 표시]
    DisplayResponse --> Listen
```

# SkillSets
- whisper (다국어모델사용)
- openai
- pyaudio


# 개발 checklist
- [x] 마이크 활용하여 사용자 질문을 받음
    - [x] 마이크 대기 - 약속된단어로 시작, 약속된 단어로 종료
    - [x] 말하면 답장
- [x] GPT API-Key 활용 openai 라이브러리 연결
- [x] 마이크를 통해 활용한 질문을 GPT에 질문을 한다.
- [x] 답은 화면에서 확인
- [x] 답변이 다되면 다시 대기상태로