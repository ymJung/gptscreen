import os
import speech_recognition as sr
import openai
import tkinter as tk
from tkinter import scrolledtext
import configparser
import threading
import time

# 설정 파일 로드
config = configparser.ConfigParser()
config.read('config.cfg', encoding='utf-8')

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.client = openai.OpenAI(api_key=config['openai']['TOKEN'])
        self.listening = True
        self.START_KEYWORD = "어이"
        self.END_KEYWORD = "오버"
        self.setup_gui()

    # GUI 관련 함수들
    def setup_gui(self):
        """GUI 초기 설정"""
        self.window = tk.Tk()
        self.window.title("GPT Screen")
        self.window.geometry("800x600")
        self._create_widgets()
        self._configure_tags()

    def _create_widgets(self):
        """GUI 위젯 생성"""
        self.status_label = tk.Label(self.window, text="마이크 대기 중...", font=("Arial", 12), fg="black")
        self.status_label.pack(pady=10)

        self.text_area = scrolledtext.ScrolledText(self.window, width=70, height=30)
        self.text_area.pack(pady=10, padx=10)

        self.quit_button = tk.Button(self.window, text="종료", command=self.window.quit)
        self.quit_button.pack(pady=10)

    def _configure_tags(self):
        """텍스트 영역의 태그 설정"""
        self.text_area.tag_configure("keyword", foreground="red")

    def update_status(self, message, color="black"):
        """상태 메시지 업데이트"""
        self.status_label.config(text=message, fg=color)
        self.window.update()

    def update_response(self, message):
        """응답 텍스트 업데이트"""
        self.text_area.insert(tk.END, f"\n{message}\n")
        self.text_area.see(tk.END)
        self.window.update()

    # 음성 인식 관련 함수들
    def listen_for_speech(self):
        """음성 인식 메인 루프"""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.listening:
                try:
                    self.update_status("마이크 대기 중...", "black")
                    audio = self.recognizer.listen(source)
                    text = self._recognize_speech(audio)
                    
                    if self.START_KEYWORD in text:
                        self._handle_start_keyword(text, source)
                    else:
                        self._display_normal_text(text)

                except sr.UnknownValueError:
                    continue
                except sr.RequestError:
                    self.update_status("음성 인식 서비스 오류", "red")
                    continue

    def _recognize_speech(self, audio):
        """음성을 텍스트로 변환"""
        return self.recognizer.recognize_google(audio, language='ko-KR')

    def _handle_start_keyword(self, text, source):
        """시작 키워드 감지 시 처리"""
        print("시작 키워드 감지됨:", text)
        self._display_keyword_text(text)
        self.update_status("질문 대기중...", "red")
        print("질문 수집 시작...")
        question = self._collect_question(source)
        
        if question.strip():
            print("질문 수집 완료:", question)
            self.update_status("생성중...", "red")
            self.ask_gpt(question.strip())
            self.update_status("마이크 대기 중...", "black")
        else:
            print("질문이 비어있음")
            self.update_status("마이크 대기 중...", "black")

    def _collect_question(self, source):
        """사용자의 질문 수집"""
        question = ""
        last_voice_time = time.time()  # 마지막 음성 인식 시간 초기화
        
        while True:
            current_time = time.time()
            # 5초 이상 침묵이고 질문이 있으면 처리
            if current_time - last_voice_time > 5 and question.strip():
                print("5초 이상 침묵 감지")
                return question.strip()
                
            try:
                print("음성 입력 대기 중...")
                audio = self.recognizer.listen(source, phrase_time_limit=3)  # 최대 3초 단위로 음성 인식
                text = self._recognize_speech(audio)
                print("인식된 텍스트:", text)
                self._display_normal_text(text)
                last_voice_time = time.time()  # 음성이 인식되면 시간 갱신
                
                # 끝 키워드가 있는 텍스트에서 끝 키워드 제거하고 질문에 추가
                if self.END_KEYWORD in text:
                    print("끝 키워드 감지됨")
                    final_text = text.replace(self.END_KEYWORD, "").strip()
                    if final_text:
                        question += final_text + " "
                    return question.strip()
                
                question += text + " "
            except sr.UnknownValueError:
                print("음성을 인식할 수 없음")
                continue
            except sr.RequestError as e:
                print("음성 인식 서비스 오류:", str(e))
                continue

    def _display_keyword_text(self, text):
        """키워드가 포함된 텍스트 표시"""
        start_idx = text.find(self.START_KEYWORD)
        end_idx = start_idx + len(self.START_KEYWORD)
        
        self.text_area.insert(tk.END, text[:start_idx])
        self.text_area.insert(tk.END, self.START_KEYWORD, "keyword")
        self.text_area.insert(tk.END, text[end_idx:] + "\n")

    def _display_normal_text(self, text):
        """일반 텍스트 표시"""
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.see(tk.END)
        self.window.update()

    # GPT 통신 관련 함수
    def ask_gpt(self, question):
        """GPT API를 통한 응답 요청"""
        try:
            self.update_response(f"질문: {question}")
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": question}
                ]
            )
            
            answer = response.choices[0].message.content
            self.update_response(f"답변: {answer}\n{'-'*50}")
            
        except Exception as e:
            self.update_response(f"오류 발생: {str(e)}")

    # 메인 실행 함수
    def run(self):
        """음성 비서 실행"""
        thread = threading.Thread(target=self.listen_for_speech)
        thread.daemon = True
        thread.start()
        self.window.mainloop()

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()
