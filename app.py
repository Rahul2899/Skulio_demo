from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def home():
    return render_template("index.html", title="Welcome to Skulio")

@app.route("/features")
def features():
    return render_template("features.html", title="Features")

@app.route("/about")
def about():
    return render_template("about.html", title="About Us")

def send_email(name, email, message):
    sender_email = "your-email@gmail.com" 
    sender_password = "your-app-password"  
    receiver_email = "rramraje02@gmail.com"     

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"New Contact Form Submission from {name}"

    body = f"""
    New contact form submission:
    
    Name: {name}
    Email: {email}
    Message: {message}
    """
    
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]
        
        if send_email(name, email, message):
            return render_template("contact.html", 
                                title="Contact Us", 
                                success=True)
        else:
            return render_template("contact.html", 
                                title="Contact Us", 
                                error=True)
            
    return render_template("contact.html", title="Contact Us")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        organization = request.form["organization"]
        # Handle form submission (e.g., save user details)
        return redirect(url_for("features"))
    return render_template("signup.html", title="Sign Up for Demo")

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    app.run(debug=True)