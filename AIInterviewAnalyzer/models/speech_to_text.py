import speech_recognition as sr


class SpeechToText:

    def __init__(self):
        self.recognizer = sr.Recognizer()

    def recognize_from_microphone(self):

        with sr.Microphone() as source:

            print("Listening...")

            self.recognizer.adjust_for_ambient_noise(source)

            audio = self.recognizer.listen(source)

        try:

            text = self.recognizer.recognize_google(audio)

            return {
                "success": True,
                "text": text
            }

        except sr.UnknownValueError:

            return {
                "success": False,
                "text": "Could not understand audio."
            }

        except sr.RequestError:

            return {
                "success": False,
                "text": "Speech service unavailable."
            }