import pyttsx3
import datetime
import requests
from bs4 import BeautifulSoup
import time
import re

# ------------------- TEXT TO SPEECH (TTS) -------------------
engine = pyttsx3.init()

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# ------------------- TIME -------------------
def get_time_text():
    now = datetime.datetime.now().strftime("%I:%M %p")
    return f"The current time is {now}."

# ------------------- DATE -------------------
def get_date_text():
    today = datetime.date.today().strftime("%B %d, %Y")
    return f"Today's date is {today}."


# ------------------- WEATHER (FAKE SIMPLE DATA) -------------------
def get_weather_text(city):
    # Simple fake response (no external API required)
    return f"The weather in {city} is warm with light clouds."

# ------------------- NEWS (SCRAPED) -------------------
def get_news_text():
    """
    Returns some sample news headlines.
    This version does NOT need internet or any API.
    """

    headlines = [
        "India reports strong growth in the technology sector this year.",
        "New artificial intelligence tools are transforming software development.",
        "Data science and machine learning skills are in high demand in the job market.",
        "Electric vehicles adoption is increasing rapidly across major cities.",
        "Space research missions from India are receiving global appreciation."
    ]

    # You can choose how many headlines to speak
    top_n = 3
    selected = headlines[:top_n]

    msg = "Here are some sample headlines: " + " ".join(selected)
    return msg

# ------------------- REMINDER SYSTEM -------------------
reminders = []

def add_reminder(text, minutes):
    remind_time = time.time() + (minutes * 60)
    reminders.append((text, remind_time))
    return f"Reminder set for {minutes} minute(s) from now."

def check_reminders():
    current = time.time()
    due = []

    for reminder_text, remind_time in reminders:
        if current >= remind_time:
            due.append((reminder_text, remind_time))

    for r in due:
        reminders.remove(r)
        msg = f"Reminder: {r[0]}"
        print(msg)
        speak(msg)

# ------------------- MAIN LOGIC -------------------
def listen_command():
    # Mic unavailable → type your command
    print("Mic / PyAudio problem: Could not find PyAudio; check installation")
    print("Assistant: Microphone is not available on this system. Please type your command.")
    cmd = input("You: ")
    return cmd.lower()

def main():
    speak("Hello Parth, your assistant is now active.")

    print("Type commands like:")
    print("- 'time' -> get current time")
    print("- 'date' -> get today's date")
    print("- 'weather in delhi'")
    print("- 'news' -> sample news headlines")
    print("- 'set reminder in 1 minute to drink water'")
    print("- 'exit' or 'quit' to stop")

    while True:
        check_reminders()
        command = listen_command()

        if "time" in command:
            msg = get_time_text()
            print(msg)
            speak(msg)

        elif "date" in command:
            msg = get_date_text()
            print(msg)
            speak(msg)

        elif "weather" in command:
            if "in" in command:
                city = command.split("in", 1)[1].strip()
            else:
                city = "your city"
            msg = get_weather_text(city)
            print(msg)
            speak(msg)

        elif "news" in command:
            msg = get_news_text()
            print(msg)
            speak(msg)

        # ---------- NEW IMPROVED REMINDER CODE ----------
        elif "reminder" in command and "minute" in command:
            try:
                txt = command.lower()

                # extract minutes using regex
                match = re.search(r"reminder in (\d+)\s*minute", txt)
                if not match:
                    raise ValueError("Minutes not found")

                minutes = int(match.group(1))

                # extract the text after "minute"
                after_index = match.end()
                after = txt[after_index:].strip()

                # remove "to" if present
                if after.startswith("to "):
                    after = after[3:].strip()

                reminder_text = after or "your reminder"

                msg = add_reminder(reminder_text, minutes)
                print(msg)
                speak(msg)

            except:
                err = "Sorry, I could not understand the reminder format."
                print(err)
                speak(err)

        elif "exit" in command or "quit" in command:
            speak("Assistant stopped.")
            break

        else:
            reply = "I heard you, but I do not have a command for that."
            print(reply)
            speak(reply)

if __name__ == "__main__":
    main()
