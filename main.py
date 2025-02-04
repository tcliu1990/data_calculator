import speech_recognition as sr



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # read the audio data from the default microphone
        audio_data = r.record(source, duration=20)
        print("Recognizing...")
        # convert speech to text
        text = r.recognize_google(audio_data)
        print(text)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
