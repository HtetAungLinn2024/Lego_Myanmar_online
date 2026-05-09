# Lego Myanmar Online
### CS50 Final Project

## Video Demo
You can watch the project demo here:  
https://www.youtube.com/watch?v=_dDMaBKGe-o

---

# Overview

Lego Myanmar Online is an e-commerce web application developed using the Flask framework as my CS50 final project. The purpose of this project is to create a complete online shopping platform where users can browse Lego products, manage their shopping cart, place orders, and make payments through a modern and user-friendly interface.

The application includes both customer and administrator functionalities. Customers can create accounts, log in securely, search for products, add items to their cart, and track their orders. Administrators can manage products, customers, and order statuses through an admin dashboard.

This project demonstrates both backend and frontend web development skills using Flask, SQLite, Bootstrap, JavaScript, and Jinja templates.

---

# Features

## 1. User Authentication
- User registration and login system
- Secure password hashing using Werkzeug
- Session management with Flask-Login
- Profile page with profile photo upload
- Password changing system

## 2. Product Management
- Admin can add, update, and delete products
- Multiple product image support
- Product detail page
- Product categories and hashtags
- Flash sale support
- Search functionality

## 3. Shopping Cart
- Add items to cart
- Remove items from cart
- Increase or decrease quantity using AJAX
- Real-time cart total updates

## 4. Order System
- Place orders
- View order history
- Track delivery progress
- Admin order status management

## 5. Payment Integration
- Payment integration using IntaSend API
- Payment tracking support

## 6. Responsive Design
- Built using Bootstrap 5
- Mobile-friendly layout
- Responsive navigation and product pages

---

# Technologies Used

## Backend
- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- SQLite

## Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- jQuery
- Jinja2 Templates

## Other Tools
- Font Awesome
- Bootstrap Icons
- IntaSend Payment API

---

# Installation

## Prerequisites
Make sure the following are installed:

- Python 3.12 or later
- pip

Required Python packages:

- Flask==3.1.0
- Flask-SQLAlchemy==3.1.1
- Flask-Login==0.6.3
- Flask-WTF==1.2.2
- WTForms==3.2.1
- Werkzeug==3.1.3
- SQLAlchemy==2.0.40
- email-validator==2.2.0
- intasend-python==1.1.2

---

# Setup

## 1. Clone the Repository

```bash
git clone https://github.com/HtetAungLinn2024/Lego_Myanmar_online.git
cd Lego_Myanmar_online
```

## 2. Create a Virtual Environment

### Linux / Mac
```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Run the Application

```bash
python main.py
```

The application will run at:

```text
http://127.0.0.1:5000/
```

---

# Project Structure

```text
Lego_Myanmar_online/
│
├── instance/
│   └── database.sqlite3
│
├── media/
│   ├── background.jpg
│   ├── profile.jpg
│   └── ...
│
├── website/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   └── ...
│   │
│   ├── __init__.py
│   ├── admin.py
│   ├── auth.py
│   ├── forms.py
│   ├── models.py
│   └── views.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

# Important Files

| File | Description |
|------|-------------|
| `models.py` | Database models for users, products, cart, and orders |
| `views.py` | Main application routes |
| `auth.py` | Authentication system |
| `admin.py` | Admin management routes |
| `forms.py` | Flask-WTF forms |
| `templates/` | HTML templates |
| `static/` | CSS, JavaScript, and images |

---

# Design Choices

One of the main design goals of this project was simplicity and usability. The interface was designed to look similar to modern e-commerce websites while remaining easy to navigate.

AJAX was used in the shopping cart system to update quantities without refreshing the page, improving user experience. Bootstrap 5 was chosen to make the website responsive across different devices.

The application structure separates authentication, admin logic, database models, and views into different files to improve code organization and maintainability.

---

# CS50 Compliance

This project satisfies the CS50 final project requirements by including:

- A complete web application using Flask
- User authentication and database management
- Frontend and backend integration
- Original project structure and implementation
- Responsive UI design
- Full project documentation
- A demonstration video

Some debugging help and guidance were assisted by ChatGPT Free Version, but the project design, implementation, and logic were created and developed by myself.

---

# Future Improvements

- Online payment confirmation
- Product reviews and ratings
- Wishlist system
- Better admin analytics dashboard
- Product filtering and sorting
- Email verification system

---

# License

This project is licensed under the MIT License.

---

# Contact

For questions or feedback:

Email: hakryuuren412@gmail.com

GitHub:  
https://github.com/HtetAungLinn2024