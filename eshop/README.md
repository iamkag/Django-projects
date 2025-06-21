# 🛒 Django eShop

A simple e-commerce web application built with Django. It features user authentication, product listings, a shopping cart, and the ability to purchase items.

## 📦 Features

- User registration and login/logout
- Product listing and details
- Shopping cart management
- Checkout and purchase flow
- Admin interface to manage products

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip
- Virtualenv (optional but recommended)
- PostgreSQL or SQLite

### Installation

1. Clone the repository:

```bash
git clone https://github.com/iamkag/django-eshop.git
cd django-eshop
```

2. Create and activate a virtual environment:

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python manage.py migrate
```

5. Create a superuser for admin access:

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser to view the app.

## 🗃️ Project Structure

```
django-eshop/
├── manage.py
├── eshop/               # Main app
├── templates/           # HTML templates
├── static/              # CSS/JS/images
├── db.sqlite3           # Default DB (can switch to PostgreSQL)
├── requirements.txt
└── README.md
```
