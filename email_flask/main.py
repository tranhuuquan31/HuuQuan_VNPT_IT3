# importing libraries
from flask import Flask, render_template, request
from flask_mail import Mail, Message
   
app = Flask(__name__)
mail = Mail(app) # instantiate the mail class
   
# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'tranhuuquan20@gmail.com'
app.config['MAIL_PASSWORD'] = 'vgbcscznxugsenge'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
   
# message object mapped to a particular URL ‘/’
@app.route("/")
def index():
  return render_template("form.html")
@app.route("/result", methods= ['POST', 'GET'])
def result():
    # if request.methods == "POST":
        msg = Message(request.form.get("Subject"), sender ='tranhuuquan20@gmail.com', recipients = [request.form.get("Email")])
        msg.body = "Gửi anh Thơ dễ thương và anh Vũ xinh đẹp nhiệm vụ gửi mail bằng flask"
        with app.open_resource ("anhvu.png") as fp:
             msg.attach("anhvu.png", "image/png", fp.read())
        mail.send(msg)
        return render_template("result.html", result = "Success!")
    # else:
    #     return render_template("result.html", result = "Failure!")
        

if __name__ == '__main__':
   app.run(debug = True)