import json
import re
import random
import tkinter as tk
import openai


def load_json(file):
    with open(file) as bot_responses:
        print(f"Loaded '{file}' successfully!")
        return json.load(bot_responses)


response_data = load_json("bot.json")


def get_response(input_string):
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
    score_list = []

    for response in response_data:
        response_score = 0
        required_score = 0
        required_words = response["required_words"]

        if required_words:
            for word in split_message:
                if word in required_words:
                    required_score += 1

        if required_score == len(required_words):
            for word in split_message:
                if word in response["user_input"]:
                    response_score += 1

        score_list.append(response_score)

    best_response = max(score_list)
    response_index = score_list.index(best_response)

    if input_string == "":
        return "Please type something so we can chat :("

    if best_response != 0:
        bot_response = response_data[response_index]["bot_response"]
        if isinstance(bot_response, list):
            bot_response = random.choice(bot_response)
        return bot_response

    return random.choice(response_data)["bot_response"]


def send_message():
    user_input = user_entry.get("1.0", tk.END).strip()
    bot_response = get_response(user_input)
    chat_log.insert(tk.END, "You: " + user_input + "\n")
    chat_log.insert(tk.END, "Bot: " + bot_response + "\n")
    user_entry.delete("1.0", tk.END)


def generate_openai_response(prompt):
    openai.api_key = "use openai api key"
    model_engine = "text-davinci-003"

    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion.choices[0].text
    return response


def handle_openai_question():
    user_input = user_entry.get("1.0", tk.END).strip()
    bot_response = generate_openai_response(user_input)
    chat_log.insert(tk.END, "You: " + user_input + "\n")
    chat_log.insert(tk.END, "Bot: " + bot_response + "\n")
    user_entry.delete("1.0", tk.END)


# Create the GUI window
window = tk.Tk()
window.title("Chatbot")
window.geometry("510x630")

# Create the chat log text widget with a colored background
chat_log = tk.Text(window, height=30, width=60, background="lightgray")
chat_log.pack()

# Create the user input entry widget with a colored background and foreground
user_entry = tk.Text(window, height=3, width=50, background="black", foreground="white", wrap="none")
user_entry.pack()


# Create the send button for the chatbot
send_button_chatbot = tk.Button(window, height=2, width=5, text="Send", command=send_message, background="white", foreground="black")
send_button_chatbot.pack()

# Create the send button for the OpenAI question-answering with color
send_button_openai = tk.Button(window, height=2, width=10, text="Ask OpenAI", command=handle_openai_question, background="black", foreground="white")
send_button_openai.pack()

# Start the GUI event loop
window.mainloop()
