from flask import Flask, redirect, url_for, session
import random
from advancedDecorators import TextDecorators, HighLowGame

app = Flask(__name__)
app.secret_key = 'a_very_secret_key'

advd = TextDecorators()

@app.route('/')
def indexPage():
    session['answer'] = random.randint(0,9)
    return  "Index Page." \
            "<a href='http://127.0.0.1:5000/highlowgame'>Click Here to Start the Game.</a>"

# @app.route('/username/<path:name>')
@app.route('/username/<name>')
def greet(name):
    return  "<h1 style='text-align:center;'>Hello World.</h1>"\
            "<p>This is a paragraph</p>" \
            "<img src='https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExd2p0MWEzYjBsNXlrYTc3OTh6Zmpkdmtic3F1djk0MGVlNnV0a2c0ZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/zQR7qMJ3Esh0Y/giphy.gif' width=200 alt='...'>"


@app.route('/<name>/<int:number>')
def greet2(name,number):
    return f"Hello, {name}. {name.capitalize()} is {number} years old."


@app.route('/test')

@advd.make_bold
@advd.make_emphasis
@advd.make_underline
def test():
    return "Is this Bold, Underlined and Emphasized?"


@app.route('/highlowgame')
def highlow_game_init():
    if not session['answer']:
        session['answer'] = random.randint(0,9)
    return  "<h1>Guess number between 0 and 9.</h1>" \
            "<img src='https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif' >" \
            f"<h1>{session['answer']}</h1>"


@app.route('/highlowgame/<int:guess>')
def highlow_game(guess):
    randnumber = session['answer']
    if not randnumber:
        return redirect(url_for('highlow_game_init'))
    if guess<randnumber:
        return  "<h1>Too Low!!</h1>" \
                "<img src='https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif'>" \
                f"<h1>{randnumber}</h1>"
    elif guess>randnumber:
        return  "<h1>Too High!!</h1>" \
                "<img src='https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif'>" \
                f"<h1>{randnumber}</h1>"
    else:
        return  "<h1>Congrats You got it right</h1>" \
                "<imh src='https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif'>" \
                "<a href='http://127.0.0.1:5000/'>Click Here to Reset the Game.</a>" \
                f"<h1>{randnumber}</h1>"


game = HighLowGame()

@app.route('/highlowgame2/<int:guess2>')
@game.checker
def highlow_game2(guess2:int):
    return guess2, session['answer']

if __name__=="__main__":
    app.run(debug=True)