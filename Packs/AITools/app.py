from flask import Flask, render_template, request
import os
from prompt_claude import *
import markdown
from dotenv import load_dotenv

load_dotenv()  # Load from .env if exists

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    response_text = ""
    if request.method == 'POST':
        user_prompt = request.form['prompt']
        if user_prompt:
            # Call the function to get the response from Claude with RAG
            response_text = prompt_claude_with_rag(user_prompt)
            html_output = markdown.markdown(response_text)
        #response_text = prompt_claude_with_rag(user_prompt)

    return render_template('index.html', response=html_output)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)