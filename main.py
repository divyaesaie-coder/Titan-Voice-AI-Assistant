import tkinter as tk
import speech_recognition as sr
import win32com.client
from datetime import datetime
import google.generativeai as genai

with open("gemini_key.txt", "r") as file:
    api_key = file.read().strip()

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

recognizer = sr.Recognizer()
recognizer.pause_threshold = 1.5

speaker = win32com.client.Dispatch("SAPI.SpVoice")


def ask_gemini(prompt):

    response = model.generate_content(
        f"""
        You are Titan AI Assistant.

        Your name is Titan.

        You were created by Divya.

        User: {prompt}
        """
    )

    return response.text


def speak(text):
    output_box.insert(tk.END, f"Assistant: {text}\n")
    output_box.see(tk.END)
    root.update()

    speaker.Speak(text)


def listen():
    try:
        output_box.insert(tk.END, "🎤 Listening...\n")
        output_box.see(tk.END)
        root.update()

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source)

        command = recognizer.recognize_google(audio)

        output_box.insert(tk.END, f"You: {command}\n")
        output_box.see(tk.END)

        return command.lower()

    except sr.UnknownValueError:
        speak("I could not understand you")
        return ""

    except Exception as e:
        print(e)
        speak("An error occurred")
        return ""


def process_command(command):

    if "who are you" in command:
        speak("I am your AI voice assistant created by Divya using Python.")

    elif "what is your name" in command or "your name" in command:
        speak("My name is AI Voice Assistant.")

    elif "hello" in command or "hi" in command:
        speak("Hello. How can I help you?")

    elif "how are you" in command:
        speak("I am doing great. Thank you for asking.")

    elif "who created you" in command:
        speak("I was created by Divya using Python.")

    elif "what can you do" in command:
        speak("I can answer questions, tell time and tell date.")

    elif "time" in command:
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")

    elif "date" in command:
        today = datetime.now().strftime("%d %B %Y")
        speak(today)

    elif "exit" in command or "close" in command:
        speak("Goodbye")
        root.destroy()

    else:
        answer = ask_gemini(command)
        speak(answer)


def start_listening():
    command = listen()

    if command:
        process_command(command)


root = tk.Tk()
root.title("AI Voice Assistant")
root.geometry("700x500")

title = tk.Label(
    root,
    text="AI Voice Assistant",
    font=("Arial", 24, "bold")
)
title.pack(pady=10)

speak_button = tk.Button(
    root,
    text="🎤 Speak",
    font=("Arial", 18),
    command=start_listening
)
speak_button.pack(pady=10)

output_box = tk.Text(
    root,
    height=20,
    width=80,
    font=("Consolas", 11)
)
output_box.pack(pady=10)

root.after(1000, lambda: speak("Voice assistant started"))

root.mainloop()
