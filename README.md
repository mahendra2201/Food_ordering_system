# Food Ordering and Management System

A Flask-based web application for managing food orders with features like user registration, email verification, order placement, cart management, and integration with Razorpay for payments.

## Features

- **User Management**:
  - User registration with OTP email verification.
  - Login/logout functionality.
- **Menu Management**:
  - View menus categorized as vegetarian and non-vegetarian.
  - Add food items to the cart.
- **Order Management**:
  - Place orders from the cart.
  - View past orders.
- **Payment Integration**:
  - Razorpay API for secure payment processing.

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: MySQL
- **Email Services**: Python SMTP
- **Payment Gateway**: Razorpay API

## Installation

### Prerequisites

- Python 3.7+
- MySQL Server
- Razorpay API Key and Secret

### Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd flask_food_ordering
   ```

2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the database connection in the `db` dictionary:
   ```python
   db = {
       "host": "<host>",
       "user": "<username>",
       "password": "<password>",
       "database": "<database_name>"
   }
   ```

4. Set up Razorpay credentials:
   ```python
   razorpay_key_id = "<your_razorpay_key_id>"
   razorpay_key_secret = "<your_razorpay_key_secret>"
   ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Access the application in your browser:
   ```
   http://127.0.0.1:5000
   ```

## Project Structure

```
.
├── static/
│   └── images/          # Images for menu items
├── templates/
│   ├── home.html        # Homepage
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   ├── menu.html        # Menu display page
│   └── ...              # Other templates
├── app.py               # Flask application
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## Key Endpoints

- `/` or `/home`: Homepage
- `/login`: Login page
- `/register`: Registration page
- `/menu`: Display full menu
- `/veg`: Display vegetarian menu
- `/nonveg`: Display non-vegetarian menu
- `/add_to_cart`: Add item to cart
- `/cartpage`: View cart
- `/orders`: View user orders

## Database Tables

- **`register`**: Stores user details.
- **`cart_<username>`**: Stores cart items for individual users.
- **`order_<username>`**: Stores orders for individual users.
- **`login`**: Tracks user login activity.

## Razorpay Integration

This project integrates Razorpay for handling online payments. Ensure you set up your API credentials and callback URLs in the Razorpay Dashboard.

## Future Enhancements

- Add user profile management.
- Implement search and filter options for menu items.
- Integrate a delivery tracking system.
- Enhance UI/UX with responsive design.


