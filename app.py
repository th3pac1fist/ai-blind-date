from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import openai
import random

app = Flask(__name__)
app.secret_key = 'some_random_secret_key'  # You can replace this with a more secure key

# Dictionary of prompts using the girl's first name as the key
blind_dates = {
    "Cat": "You are on a date with Cat, a 23-year-old software engineer from a large tech company. She studied computer science at MIT and loves to say 'em...' at the end of her sentences.",
    "Sophia": "You are on a date with Sophia, a 28-year-old artist who loves to paint landscapes. She's traveled to over 30 countries and has a cat named Whiskers.",
    "Emma": "You are on a date with Emma, a 26-year-old yoga instructor. She's vegan, loves nature, and has a passion for mindfulness and meditation.",
    "Olivia": "You are on a date with Olivia, a 30-year-old journalist. She's a bookworm, enjoys indie music, and has a penchant for vintage fashion.",
    "Ava": "You are on a date with Ava, a 27-year-old veterinarian. She loves animals, enjoys hiking, and is a fan of classic rock music."
}

current_date = random.choice(list(blind_dates.keys()))
messages = [{"role": "system", "content": blind_dates[current_date]}]

@app.route('/')
def index():
    api_key_set = 'openai_api_key' in session
    return render_template('template.html', api_key_set=api_key_set, current_date=current_date, intro_message=blind_dates[current_date])

@app.route('/set_api_key', methods=['GET', 'POST'])
def set_api_key():
    if request.method == 'POST':
        session['openai_api_key'] = request.form['api_key']
        openai.api_key = session['openai_api_key']
        return redirect(url_for('index'))
    return render_template('template.html', api_key_set=False)

@app.route('/chat', methods=['POST'])
def chat():
    global current_date, messages
    user_message = request.form['message']
    
    if user_message.lower() in ["next", "move on", "next date"]:
        current_date = random.choice(list(blind_dates.keys()))
        messages = [{"role": "system", "content": blind_dates[current_date]}]
        return jsonify({"message": f"You are now on a date with {current_date}.", "current_date": current_date})
    
    messages.append({"role": "user", "content": user_message})
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    ai_message = response.choices[0].message['content']
    messages.append({"role": "assistant", "content": ai_message})
    
    return jsonify({"message": ai_message})

if __name__ == "__main__":
    app.run(debug=True)
