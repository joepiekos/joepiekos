from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route('/')
def index():
    messageBethan = "hellooooo love you"
    random_number = random.randint(1, 100)  # Generates a random number between 1 and 100
    return render_template('index.html', number=random_number,message = messageBethan)

if __name__ == '__main__':
    app.run(debug=True)