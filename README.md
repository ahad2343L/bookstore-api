# 📚 BookStore API

A lightweight BookStore API built with Django. This API allows you to manage book listings, genres, authors (with image support), and user carts. It is ideal for learning, personal projects, or as a foundation for building a full-featured e-commerce bookstore.

---

## 🚀 Features

- 📖 Book listing with details
- 🏷️ Genre/category management
- 👨‍💼 Author listing with image upload
- 🛒 Cart functionality (add/remove items)

> ❌ This project does **not** include:
> - Order processing
> - Payment integration
> - Background tasks

---

## 🛠️ Tech Stack

- **Backend:** Django (Django REST Framework)
- **Database:** SQLite (default) or PostgreSQL
- **Media Handling:** Django’s `ImageField`

---

## 📦 Installation

1. Clone the repo

```
git clone https://github.com/your-username/bookstore-api.git
cd bookstore-api
```
2.Create a virtual environment
```
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```
3.Install dependencies
```
pip install -r requirements.txt
```
4.Apply migrations
```
python manage.py migrate
```
5.Run the development server
```
python manage.py runserver
```
📂 Project Structure
```
bookstore-api/
├── manage.py
├── .venv/                   # Virtual environment
├── media/                   # Uploaded images
├── core/                    # Project settings (settings.py, urls.py, wsgi.py)
├── authentication/          # Handles user registration/login
├── store/                   # Handles books, genres, authors, cart
```


📮 API Endpoints Overview
```
Method	Endpoint	Description
GET	/api/books/	List all books
POST	/api/books/	Add a new book
GET	/api/genres/	List all genres
POST	/api/genres/	Create a new genre (admin only)
GET	/api/authors/	List all authors
GET	/api/cart/	View user's cart
POST	/api/cart/	Create a new cart ID
POST	/api/cart/{id}/items/	Add item to cart by cart ID
```

## License
This project is open-source and free to use.

## Author
Developed by Abdul Ahad.
