from flask import Flask, render_template, request
import os
from Packs.AITools.xsiam_content_readme.prompt_claude import *
import markdown
from dotenv import load_dotenv
from flask import jsonify

load_dotenv()  # Load from .env if exists

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_prompt = request.form['prompt']
        if user_prompt:
            # Call Claude API synchronously and return result
            response_text = prompt_claude_with_rag(user_prompt)
            html_output = markdown.markdown(response_text)
            return render_template('index.html', response=html_output, loading=False, prompt=user_prompt)
    return render_template('index.html', response="", loading=False)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)