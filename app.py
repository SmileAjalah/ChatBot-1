from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv
from datetime import datetime

# https://platform.openai.com/account/api-keys
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

# print(openai.api_key)

# Set up Flask app
app = Flask(__name__)


# Define the home page route
@app.route("/")
def home():
    return render_template("index.html")

# Define the chatbot route
@app.route("/chatbot", methods=["POST"])
def chatbot():
    # pass

    # Get the message input from the user
    user_input = request.form["message"]
    # time_input = request.post["message"]
    # return render_template('chatbot.html', user_input=user_input)

    date_time = datetime.now()
    date = date_time.strftime("%H:%M")
    # return str(date_time)
    # return render_template('chatbot.html', date=date)

    # Use the OpenAI API to generate  a response
    prompt = f"User: {user_input}\nChatbot: "
    chat_history = []
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        stop=["\nUser: ", "\nChatbot: "]
    )

    # Extract the response text from the OpenAI API result
    bot_response = response.choices[0].text.strip()

    # Add the user input and bot response to the chat history
    chat_history.append(f"User: {user_input}\nChatbot: {bot_response}")

    # Render the Chatbot template with the response text
    return render_template(
        "chatbot.html",
        user_input=user_input,
        bot_response=bot_response,
        date=date
    )

# Start the Flask app
if __name__ == "__main__":
    app.run(debug=True)