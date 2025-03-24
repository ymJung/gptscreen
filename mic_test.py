import speech_recognition as sr

def test_microphone():
    recognizer = sr.Recognizer()
    print("사용 가능한 마이크 목록:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"마이크 {index}: {name}")
    
    try:
        with sr.Microphone() as source:            
            recognizer.adjust_for_ambient_noise(source, duration=1) # 소음 체크 
            audio = recognizer.listen(source, timeout=5) # 5초 녹음
            text = recognizer.recognize_google(audio, language='ko-KR')
            print(f"인식된 텍스트: {text}")
            
    except sr.WaitTimeoutError:
        print("fail. 음성x.")
    except sr.UnknownValueError:
        print("fail 인식실패")
    except sr.RequestError as e:
        print(f"API 요청 오류: {e}")
    except Exception as e:
        print(f"오류: {e}")

if __name__ == "__main__":
    test_microphone()
