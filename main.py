import speech_recognition as sr

# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()

while True:
    command = input("Enter 's' to start listening, 'q' to quit: ")
    if command.lower() == 's':
        # Reading Microphone as source
        # listening the speech and store in audio_text variable
        with sr.Microphone() as source:
            print("Listening...")
            audio_text = r.listen(source)
            print("Finished listening.")
        # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        try:
            # using sphinx recognition
            print("Text: "+r.recognize_sphinx(audio_text))
        except:
            print("Sorry, I did not get that")
    elif command.lower() == 'q':
        break