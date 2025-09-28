from flask import Flask, render_template, request
import requests
import smtplib
import dotenv, os

# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()
app = Flask(__name__)

dotenv.load_dotenv(
    "/home/ghostyking/Projects/Python100Days/Python-Learning-Journey/.env"
)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["POST","GET"])
def contact():
    message = False
    if request.method == "POST":
        data = request.form
        message = True
        msg = f"Subject: New Message\n\nName: {data["name"]}\nEmail: {data["email"]}\nPhone: {data["phone"]}\nMessage: {data["message"]}"
        print(msg)

        mail_usercontacts(msg)
        return render_template("contact.html", msg_sent = message )
    return render_template("contact.html", msg_sent = message)

def mail_usercontacts(message):
    my_email = os.getenv("MY_EMAIL")
    password = os.getenv("MY_EMAIL_PASSWORD")
    to_mail = os.getenv("TO_MAIL")
    with smtplib.SMTP("smtp.gmail.com") as connection:
    
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs=to_mail, msg=message)

# @app.route("/form-entry")
# def receive_contact_data():
#     pass


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
