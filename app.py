from flask import Flask, request, render_template
import pymysql
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import razorpay
razorpay_key_id="rzp_test_zBe6YsIVVwQD1T"
razorpay_key_secret="t4I4wMMdDBeRoZI9ZDPu8qoC"
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
@app.route("/registerdata",methods=["POST","GET"])
def registerdata():
    if request.method=="POST":
        name=request.form['name']
        username=request.form['username']
        email=request.form['email']
        mobile=request.form['mobile']
        password=request.form['password']
        cpassword=request.form['confirm-password']
        """
        print(name)
        print(username)
        print(email)
        print(mobile)
        print(password)
        print(cpassword)
        """
        if password==cpassword:
            otp1 = random.randint(111111, 999999)
            global verify_otp
            verify_otp=str(otp1)
            from_email = 'mannem.mahendra2407@gmail.com'
            to_email = email
            subject = 'OTP For Validation'
            body = f'OTP for Validation is {verify_otp}'

            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', '587')
            server.starttls()
            server.login('mannem.mahendra2407@gmail.com', 'dsju jftf aqnd wtje')
            server.send_message(msg)
            server.quit()

            return render_template("verifyemail.html",name = name,username=username,email=email,mobile=mobile,password=password)
        else:
            return 'make sure that password and confirm password are same'
        
    else:
        return "<h3 style='color : red'; >Data Get in Wrong Manner</h3>"

@app.route("/verifyemail",methods=["POST","GET"])                                  
def verifyemail():
        if request.method == "POST":
            name = request.form['name']
            username=request.form['username']
            email=request.form['email']
            mobile=request.form['mobile']
            password=request.form['password']
            otp=request.form['otp']
            if(otp == verify_otp):
                try:
                    conn=pymysql.connect(**db)
                    cursor=conn.cursor()
                    q="INSERT INTO register(name,username,email,mobile,password) VALUES(%s,%s,%s,%s,%s)"
                    cursor.execute(q,(name,username,email,mobile,password))
                    conn.commit()
                except:
                    return "some random errors occured"

                else:
                    return render_template("login.html")
            else:
                return render_template("register.html")
        else:
            return "<h3 style='color : red';>Data Get in Wrong Manner</h3>"
@app.route("/userlogin",methods=["POST","GET"])
def userlogin():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        try:
            conn=pymysql.connect(**db)
            cursor=conn.cursor()
            q="select * from register where username=%s"
            cursor.execute(q,(username,))
            row=cursor.fetchone()
            if(row==None):
                return "User DOesn't Exist,Create Account First"
            else:
                if password!=row[4]:
                    return "Incorrect Password"
                else:
                        conn=pymysql.connect(**db)
                        cursor=conn.cursor()
                        q="INSERT Into userlogin(username,password) values(%s,%s)"
                        cursor.execute(q,(username,password))
                        conn.commit()
                        return render_template("userhome.html",name=username)

        except:
            return "some random errors occured"

        else:
            return render_template("login.html")
    else:
        return "<h3 style='color : red';>Data Get in Wrong Manner</h3>"


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
@app.route("/add_to_cart", methods=["POST", "GET"])
def add_to_cart():
    if request.method == "POST":
        try:
            user1 = request.args.get('username')
            fooditem = request.form["fooditem"]
            quantity = request.form["quantity"]
            price = request.form["price"]

            if not user1 or not fooditem or not quantity or not price:
                raise ValueError("Missing required input data.")

            totalprice = str(int(price) * int(quantity))

            conn = pymysql.connect(**db)
            cursor = conn.cursor()
            q1 = "SELECT * FROM cart WHERE username = %s AND fooditem = %s"
            cursor.execute(q1, (user1, fooditem))
            row = cursor.fetchone()
            print(row)

            if row:
                update_quantity = str(int(row[2]) + int(quantity))
                updated_total_price = str(int(row[4]) + int(totalprice))
                q2 = "UPDATE cart SET quantity = %s, total_price = %s WHERE fooditem = %s AND username = %s"
                cursor.execute(q2, (update_quantity, updated_total_price, fooditem, user1))
            else:
                q = "INSERT INTO cart (username, fooditem, quantity, price, total_price) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(q, (user1, fooditem, quantity, price, totalprice))

        except pymysql.MySQLError as db_error:
            return f"Database error occurred: {str(db_error)}", 500
        except ValueError as value_error:
            return f"Input validation error: {str(value_error)}", 400
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}", 500
        finally:
            if 'conn' in locals() and conn.open:
                conn.commit()
                conn.close()

        return menu()
    else:
        return "<h3 style='color: red;'>Invalid request method</h3>", 405

@app.route("/cartpage", methods=["GET"])
def cartpage():
    username = request.args.get('username')
    if not username:
        return "Username is required", 400

    try:
        conn = pymysql.connect(**db)
        cursor = conn.cursor()
        q = "SELECT * FROM cart WHERE username = %s"
        cursor.execute(q, (username,))
        rows = cursor.fetchall()
        
        grand_total = sum(int(row[4]) for row in rows)
        amount_in_paise = grand_total * 100

        order = client.order.create({
            'amount': amount_in_paise,
            'currency': 'INR',
            'payment_capture': '1'
        })
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return "CART IS EMPTY", 500
    finally:
        cursor.close()
        conn.close()

    return render_template("cart.html", data=rows, grand_total=grand_total, order=order, name=username)

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
        user1 = request.args.get('username')
        if(user1 is None):
            return "User Not Found"
        else:
            conn=pymysql.connect(**db)
            cursor=conn.cursor()
            q="truncate table cart"
            cursor.execute(q)
            conn.commit()
            conn.close()
            return render_template("sucess.html") 
    
    except:
        return render_template("failure.html")


if __name__ == "__main__":
    app.run(port=5001)