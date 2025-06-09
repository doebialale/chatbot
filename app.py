from flask import Flask, render_template, request

app = Flask(__name__)

# Initialize an empty list to store the chat history
chat_history = []

@app.route('/')
def index():
    return render_template('index.html', chat_history=chat_history)

@app.route('/submit', methods=['POST'])
def submit():
    user_message = request.form['user_message']
    
    # Add the user's message to the chat history
    chat_history.append({'sender': 'You', 'message': user_message})

    # Simulate a bot response (replace this with your actual bot logic)
    bot_response = "I'm a simple echo bot. Type something else!"

    # Add the bot's response to the chat history
    chat_history.append({'sender': 'Chatbot', 'message': bot_response})

    return render_template('index.html', chat_history=chat_history)

if __name__ == '__main__':
    app.run(debug=True)
