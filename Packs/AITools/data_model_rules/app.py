from flask import Flask, render_template, request
from prompt_claude import *
import markdown
from dotenv import load_dotenv
from flask import jsonify

load_dotenv()  # Load from .env if exists

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', response="", loading=False)

@app.route('/api/claude', methods=['POST'])
def api_claude():
    data = request.get_json()
    user_prompt = data.get('prompt', '')
    if not user_prompt:
        return jsonify({'error': 'Prompt is required.'}), 400
    response_text = prompt_claude_with_rag(user_prompt)
    html_output = markdown.markdown(response_text)
    return jsonify({'response': html_output})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)