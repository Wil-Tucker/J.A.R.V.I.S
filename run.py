import speech_recognition as sr
import openai
from elevenlabs import generate, stream, set_api_key
import tkinter as tk
from tkinter import font as tkFont
import threading
from dotenv import load_dotenv
import os

#Load the .env file
load_dotenv()


#Mic input - https://github.com/Uberi/speech_recognition/blob/master/examples/microphone_recognition.py
def get_speech_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for voice input")
        audio_input = recognizer.listen(source)
        try:
            spoken_text = recognizer.recognize_google(audio_input)
            print(f"You said: {spoken_text}")
            return spoken_text
        except sr.UnknownValueError:
            print("Voice input failed.")
            return None
        except sr.RequestError as e:
            print(f"Error occurred: {e}")
            return None


#Sending input to OpenAI - https://platform.openai.com/docs/guides/text-generation
def get_openai_response(spoken_text):
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_client = openai.OpenAI(api_key=openai_api_key)

    #Need to limit tokens for Eleven Labs API max usage.
    prompt = "You are JARVIS, a formal and intelligent virtual assistant. Respond in a CONCISE manner."

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": spoken_text}
        ]
    )

    jarvis_reply = response.choices[0].message.content
    print(f"JARVIS: {jarvis_reply}")
    return jarvis_reply



#Text-to-speech using ElevenLabs - https://github.com/elevenlabs/elevenlabs-python
def speak_response(jarvis_reply):
    elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
    set_api_key(elevenlabs_api_key)

    #Matthew provides a solid, formal voice
    audio_output = generate(
        text=jarvis_reply,
        voice="Matthew",
        model="eleven_monolingual_v1",
        stream=True
    )
    stream(audio_output)



#Integrating all modules with Tkinter UI - https://tkdocs.com/tutorial/
def main():
    def pressed_speak_button():
        #Disable speak button once pushed
        speak_button.config(state=tk.DISABLED, bg="#002043")

        def separateThreadTask():
            spoken_text = get_speech_input()
            if spoken_text:
                response_text = get_openai_response(spoken_text)
                speak_response(response_text)
            #Re-enable speak button once J.A.R.V.I.S response is finished
            speak_button.config(state=tk.NORMAL, bg="#00caff")

        #Run on separate thread to stop 'Not-Responding' window issue
        threading.Thread(target=separateThreadTask).start()

    #General UI Customisation
    root = tk.Tk()
    root.title("J.A.R.V.I.S")
    root.geometry('250x150') #Window dimensions in pixels
    root.config(bg="#121212")

    customFont = tkFont.Font(family="Helvetica", size=14)  #Custom font

    #Customising the speak button
    speak_button = tk.Button(root, text="Speak", command=pressed_speak_button, font=customFont, bg="#00caff", fg="white", activebackground="#00caff", activeforeground="white")
    #Align the button the middle of the user interface
    speak_button.pack(pady=14, expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()