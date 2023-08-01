from tkinter import *
import re
import pyttsx3
import responses
import smtplib
import os
import speech_recognition as sr

r = sr.Recognizer()

welcome = pyttsx3.init()
rate = welcome.getProperty('rate')
welcome.setProperty('rate', 140)
voice = welcome.getProperty('voices')
welcome.setProperty('voice', voice[1].id)
welcome.say("Welcome to our chat bot . I am TAB and here to assist you.")
welcome.runAndWait()
welcome.say("Please type into the textbox")
welcome.runAndWait()


def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainty += 1
    percentage = float(message_certainty) / float(len(recognised_words))

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_messages(message):
    highest_prob_list = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    response(responses.R_GREET(), ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
    response(responses.R_FAREWELL(), ['bye', 'goodbye'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('You\'re welcome!. Have a good day', ['thank', 'thanks'], single_response=True)
    response('I love you too.', ['i', 'love', 'bot', 'you'], required_words=['love', 'bot'])
    response(responses.R_ADVICE, ['give', 'advice'], required_words=['advice'])
    response(responses.R_EATING, ['what', 'you', 'have', 'eat', 'lunch', 'dinner'], required_words=['you', 'eat'])
    response(responses.R_ASSISTANCE(), ['help', 'assistance', 'what', 'can', 'you', 'do', 'how'],
             required_words=['assistance'])
    response(responses.R_ASSISTANCE(), ['help', 'assistance', 'what', 'can', 'you', 'do', 'how'],
             required_words=['help'])
    response(responses.R_NOTE, ['open', 'notepad', 'note', 'make'], required_words=['notepad'])
    response(responses.R_NOTE, ['open', 'notepad', 'note', 'make'], required_words=['note'])
    response('Opening calculator.', ['open', 'calculator', 'plus', 'minus', 'times', 'divided'])
    response(responses.R_EMAIL, ['open', 'email', 'compose', 'write'], required_words=['email'])
    response("Opening microsoft edge", ['open', 'microsoft', 'edge', 'google', 'search', 'look', 'find', 'out', 'up'])
    response(responses.R_SEARCH, ['search', 'find', 'look up'], required_words=['find'])
    response(responses.R_SEARCH, ['search', 'find', 'look up'], required_words=['search'])
    response(responses.R_SEARCH, ['search', 'find', 'look up', 'meaning'], required_words=['meaning'])
    response(responses.R_DAY, ['how', 'was', 'your', 'day'], required_words=['day'])
    response(responses.R_JOKE(), ['tell', 'joke', 'laugh', ], required_words=['joke'])
    response("I am not on any social media", ["insta", "instagram", "linkedin", "twitter"])
    best_match = max(highest_prob_list, key=highest_prob_list.get)

    return responses.unknown() if highest_prob_list[best_match] < 1 else best_match


def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response


root = Tk()
root.geometry("650x821")
root.title("TAB")
bg = PhotoImage(file="ok.png")
my_label = Label(root, image=bg)
my_label.place(x=0, y=0, relheight=1, relwidth=1)
text1 = Label(root, text="TAB - The Assist Bot", font="Times 24  bold")
text1.grid(row=0, column=0)
bot_response = Label(root, text="BOT RESPONSE", font="Times 16 italic")
bot_response.grid(row=6, column=0)
chat_entry = Entry(root, bg="black", fg="white", width=30, font="Times 14 normal")
chat_entry.grid(pady=20)
chat_button = Button(text="send", bg="black", fg="white", font="Times 14 normal", command=lambda: chatting())
chat_button.grid(pady=20)
speak_button = Button(text="speak", bg="black", fg="white", font="Times 14 normal", command=lambda: speak())
speak_button.grid(pady=10)


def write_note():
    os.system("notepad.exe")


def search():
    os.system("C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")


def calculate():
    os.system("calc.exe")


def send_email():
    top = Toplevel()
    top.title("SEND EMAIL")
    global img
    img = PhotoImage(file="please.png")
    my = Label(top, image=img)
    my.place(x=0, y=0, relheight=1, relwidth=1)
    top.geometry("600x420")
    receiver = Label(top, text="Receiver's Address :", font="Times 16 normal", bg="black", fg="white")
    receiver.grid(row=0, column=0, pady=10, padx=10)

    receiver_email_entry = Entry(top, width=20, font="Times 16 normal", bg="black", fg="white")
    receiver_email_entry.grid(row=0, column=1, padx=10, pady=10)

    message_label = Label(top, text="Content: ", font="Times 16 normal", bg="black", fg="white")
    message_label.grid(row=1, column=0, padx=10, pady=10)

    message = Text(top, font="Times 16 normal", bg="black", fg="white", height=7, width=30)
    message.grid(row=1, column=1, padx=10, pady=10)
    note_save = Button(top, text="SEND", font="Times 16 normal", bg="black", fg="white", command=lambda: send())
    note_save.grid(row=2, column=1)

    def send():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user="codetestsnek@gmail.com", password="glwvqvlaeagttrdo")
        connection.sendmail(from_addr="codetestsnek@gmail.com", to_addrs=receiver_email_entry.get(),
                            msg=message.get(1.0, END))
        top.destroy()


def chatting():
    response = get_response(chat_entry.get())
    bot_response["text"] = response
    welcome.say(response)
    if response == "Opening notepad":
        write_note()
    if response == "Please compose your E- mail":
        send_email()
    if response == 'Opening calculator.':
        calculate()
    if response == "Opening chrome":
        search()
    welcome.runAndWait()


def speak():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
        said = r.recognize_google(audio_data=audio, show_all=False, )
        chat_entry.delete(0, END)
        chat_entry.insert(0, said)
        chat_button.invoke()


root.mainloop()
