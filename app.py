from flask import Flask, request, render_template
import pymysql
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import razorpay
razorpay_key_id="rzp_test_HU0R8jEOshp2Rg"
razorpay_key_secret="SMyH6uWarivHOaqSLt2gSULq"
client=razorpay.Client(auth=(razorpay_key_id,razorpay_key_secret))

verify_otp = "0"
db = {
    "host": "localhost",
    "password": "root",
    "user": "root",
    "database": "sahafoods"
}

app = Flask(__name__)

@app.route("/")
def basepage():
    return render_template("home.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/contactus")
def contactus():
    return render_template("contactus.html")

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/FAQS")
def FAQS():
    return render_template("FAQS.html")

@app.route("/policies")
def policies():
    return render_template("our_policies.html")

@app.route("/logout")
def logout():
    return render_template("home.html")

@app.route("/logindata", methods=["POST", "GET"])
def logindata():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        try:
            conn = pymysql.connect(**db)
            cursor = conn.cursor()
            query = "SELECT * FROM register WHERE username=%s"
            cursor.execute(query, (username,))
            row = cursor.fetchone()

            if row is None:
                return "User doesn't exist. Please create an account first."
            elif password != row[4]:
                return "Incorrect password."
            else:
                # Insert login attempt into the login table
                query = "INSERT INTO login(username, password) VALUES(%s, %s)"
                cursor.execute(query, (username, password))
                conn.commit()  # Commit the transaction

                return render_template("userhome.html", name=username)
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            conn.close()
    else:
        return "<h3 style='color: red;'>Data sent in an incorrect manner.</h3>"


@app.route("/registerdata", methods=["POST", "GET"])
def registerdata():
    if request.method == "POST":
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']
        cpassword = request.form['confirm-password']

        if password != cpassword:
            return "<h1 style='color:red;'>Passwords do not match. Please try again.</h1>"

        try:
            conn = pymysql.connect(**db)
            cursor = conn.cursor()
            query = "SELECT * FROM register WHERE email = %s"
            cursor.execute(query, (email,))
            row = cursor.fetchone()

            if row:
                return "<h1 style='color:red;'>Given Email ID is already used. Please login or register with another email.</h1>"

            # Generate OTP
            otp1 = random.randint(111111, 999999)
            verify_otp = str(otp1)

            # Email credentials (Use environment variables instead of hardcoding)
            from_email = "mannem.mahendra2407@gmail.com"
            email_password = "dsju jftf aqnd wtje"

            # Email sending
            to_email = email
            subject = 'OTP for Validation'
            body = f'Your OTP for validation is {verify_otp}.'

            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_email, email_password)
            server.send_message(msg)
            server.quit()

            return render_template("verifyemail.html", name=name, username=username, mobile=mobile, email=email, password=password, otp=verify_otp)

        except pymysql.MySQLError as e:
            return f"<h1 style='color:red;'>Database error occurred: {str(e)}</h1>"
        except smtplib.SMTPException as e:
            return f"<h1 style='color:red;'>Failed to send email: {str(e)}</h1>"
        except Exception as e:
            return f"<h1 style='color:red;'>An unexpected error occurred: {str(e)}</h1>"
        finally:
            cursor.close()
            conn.close()
    else:
        return "<h1 style='color:red;'>Data sent in an incorrect manner.</h1>"

@app.route("/verifyemail", methods=["POST", "GET"])
def verifyemail():
    if request.method == "POST":
        name = request.form['name']
        username = request.form['username']
        mobile = request.form['mobile']
        email = request.form['email']
        password = request.form['password']
        otp = request.form['otp']

        if otp == verify_otp:
            try:
                conn = pymysql.connect(**db)
                cursor = conn.cursor()

                query = "INSERT INTO register(name, username, mobile, email, password) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(query, (name, username, mobile, email, password))
                conn.commit()
            except Exception as e:
                return f"An error occurred: {e}"
            finally:
                conn.close()
            return render_template("home.html")
        else:
            return "<h3 style='color: red;'>Incorrect OTP. Please try again.</h3>"
    else:
        return "<h3 style='color: red;'>Data sent in an incorrect manner.</h3>"

@app.route("/userhome", methods=["POST", "GET"])
def userhome():
    return render_template("userhome.html",)

@app.route("/menu", methods=["POST", "GET"])
def menu():
    username=request.args.get('username')
    items = [
        {"name": "Chicken Dum Biryani", "price": 180, "image_url": "/static/images/Hyderbad_chicken_biriyani.jpg"},
        {"name": "Cheese Cake", "price": 40, "image_url": "/static/images/chesecake.jpg"},
        {"name": "Veg Noodles", "price": 80, "image_url": "/static/images/veg_noodles.jpg"},
        {"name": "Veg Fried Rice", "price": 70, "image_url": "/static/images/veg_friedrice.jpg"},
        {"name": "Chicken Noodles", "price": 90, "image_url": "/static/images/chicken_noodles.jpg"},
        {"name": "Chicken Fried Rice", "price": 120, "image_url": "/static/images/chicken_friedrice.jpg"},
        {"name": "Chapathi", "price": 40, "image_url": "/static/images/chapathi.jpg"},
        {"name": "Butter Naan", "price": 80, "image_url": "/static/images/buter_nans.jpg"},
        {"name": "Kajju Tomato Curry", "price": 180, "image_url": "/static/images/kajju_tomato_curry.jpg"},
        {"name": "Momos", "price": 130, "image_url": "/static/images/momos.jpg"},
        {"name": "Shawarma", "price": 100, "image_url": "/static/images/shawarma.jpg"},
        {"name": "Pulkas", "price": 10, "image_url": "/static/images/Pulka's.jpg"},
        {"name": "Mutton Curry", "price": 350, "image_url": "/static/images/mutton_curry.jpg"},
        {"name": "Chicken Curry", "price": 120, "image_url": "/static/images/chicken_curry.jpg"},
        {"name": "Paneer Butter Masala Curry", "price": 230, "image_url": "/static/images/paneer_butter_masala.jpg"},
        {"name": "Japanese Ramen", "price": 250, "image_url": "/static/images/japanese_ramen.jpg"},
        {"name": "Mutton Paya Soup", "price": 350, "image_url": "/static/images/mutton_payasoup.jpg"},
        {"name": "Thandoori", "price": 450, "image_url": "/static/images/Thandoori.jpg"},
        {"name": "Chicken Wings", "price": 220, "image_url": "/static/images/chickenwings.jpg"},
        {"name": "Chicken Nuggets", "price": 230, "image_url": "/static/images/chicken_nuggets.jpg"} 
    ]
    return render_template("menu.html",items=items,name=username)
@app.route("/veg")
def vegetarian_menu():
    user2=request.args.get('username')
    vegitems = [
        {"name": "Veg Noodles", "price": 80, "image_url": "/static/images/veg_noodles.jpg"},
        {"name": "Veg Fried Rice", "price": 70, "image_url": "/static/images/veg_friedrice.jpg"},
        {"name": "Chapathi", "price": 40, "image_url": "/static/images/chapathi.jpg"},
        {"name": "Butter Naan", "price": 80, "image_url": "/static/images/buter_nans.jpg"},
        {"name": "Kajju Tomato Curry", "price": 180, "image_url": "/static/images/kajju_tomato_curry.jpg"},
         {"name": "Pulka's", "price": 10, "image_url": "/static/images/pulka's.jpg"},
        {"name": "Cheese Cake", "price": 40, "image_url": "/static/images/chesecake.jpg"},
        {"name": "Paneer Butter Masala Curry", "price": 230, "image_url": "/static/images/paneer_butter_masala.jpg"},
            {"name": "Momo's", "price": 130, "image_url": "/static/images/momos.jpg"}      
    ]
    return render_template("veg.html",items=vegitems,name=user2)

@app.route("/nonveg")
def nonvegetarian_menu():
    user1=request.args.get('username')
    nonvegitems = [
        {"name": "Chicken Dum Biryani", "price": 180, "image_url": "/static/images/Hyderbad_chicken_biriyani.jpg"},
        {"name": "Chicken Noodles", "price": 90, "image_url": "/static/images/chicken_noodles.jpg"},
        {"name": "Chicken Fried Rice", "price": 120, "image_url": "/static/images/chicken_friedrice.jpg"},
        {"name": "Mutton Curry", "price": 350, "image_url": "/static/images/mutton_curry.jpg"},
        {"name": "Shawarma", "price": 100, "image_url": "/static/images/shawarma.jpg"},
        {"name": "Japanese Ramen", "price": 250, "image_url": "/static/images/japanese_ramen.jpg"},
        {"name": "Mutton Paya Soup", "price": 350, "image_url": "/static/images/mutton_payasoup.jpg"},
        {"name": "Thandoori", "price": 450, "image_url": "/static/images/Thandoori.jpg"},
        {"name": "Chicken Wings", "price": 220, "image_url": "/static/images/chickenwings.jpg"},
        {"name": "Chicken Nuggets", "price": 230, "image_url": "/static/images/chicken_nuggets.jpg"} 

    ]
    return render_template("nonveg.html",name=user1,items=nonvegitems)



@app.route("/orders", methods=["POST", "GET"])
def orders():
    pass
@app.route("/add_to_cart",methods=["POST","GET"])
def add_to_cart():
    if request.method=="POST":
        user1=request.args.get('username')
        fooditem=request.form["fooditem"]
        quantity=request.form["quantity"]
        price=request.form["price"]
        print(user1)
        print(fooditem)
        print(quantity)
        print(price)
        totalprice=int(price)*int(quantity)
        totalprice=str(totalprice)
        print(totalprice)

        try:
            conn=pymysql.connect(**db)
            cursor=conn.cursor()
            q="INSERT Into cart(username,fooditem,quantity,price,total_price) values(%s,%s,%s,%s,%s)"
            cursor.execute(q,(user1,fooditem,quantity,price,totalprice))
            conn.commit()
        except Exception as e:
            print(e)
            return "some random errors occured"

        else:
            return menu()
    else:
        return "<h3 style='color : red';>Data Get in Wrong Manner</h3>"
@app.route("/cartpage",methods=["GET"])
def cartpage():
    username=request.args.get('username')
    print(username)
    try:
        conn=pymysql.connect(**db)
        cursor=conn.cursor()
        q="select * from cart where username=(%s)"
        cursor.execute(q,(username))
        rows=cursor.fetchall()
        print(rows)
        grand_total=0
        for i in rows:
            grand_total+=int(i[4])
            result=grand_total*100
            order=client.order.create({
                    'amount':result,
                    'currency':'INR',
                    'payment_capture':'1'
                })
        print(order)
    except:
        return "Some Random Errors Occurred"
    else:
        return render_template("cart.html",data=rows,grand_total=grand_total,order=order,name=username)
@app.route("/sucess",methods = ["POST","GET"])
def sucess():
    payment_id = request.form.get("razorpay_payment_id")
    order_id = request.form.get("razorpay_order_id")
    signature = request.form.get("razorpay_signature")
    dict1 = {
        'razorpay_order_id' : order_id,
        'razorpay_payment_id' : payment_id,
        'razorpay_signature' : signature
    }
    try:
        client.utility.verify_payment_signature(dict1)
        return render_template("sucess.html")
    except:
        return render_template("failure.html")


if __name__ == "__main__":
    app.run(port=5001)