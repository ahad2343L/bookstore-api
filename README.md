# 📚 BookStore API

A lightweight BookStore API built with Django. This API allows you to manage book listings, genres, authors (with image support), and user carts. It is ideal for learning, personal projects, or as a foundation for building a full-featured e-commerce bookstore.

---

## 🚀 Features

- 📖 Book listing with details
- 🏷️ Genre/category management
- 👨‍💼 Author listing with image upload
- 🛒 Cart functionality (add/remove items)
- 🔐 Token-based authentication (optional, if you’ve added it)

> ❌ This project does **not** include:
> - Order processing
> - Payment integration
> - Background tasks

---

## 🛠️ Tech Stack

- **Backend:** Django (Django REST Framework)
- **Database:** SQLite / PostgreSQL (your choice)
- **Media Handling:** Django’s default `ImageField`

---

## 📦 Installation

1. **Clone the repo**

```bash
git clone https://github.com/your-username/bookstore-api.git
cd bookstore-api
Create a virtual environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Apply migrations

bash
Copy
Edit
python manage.py migrate
Run the development server

bash
Copy
Edit
python manage.py runserver
📂 Project Structure
bash
Copy
Edit
bookstore-api/
├── manage.py
├── bookstore/               # Project settings
├── books/                   # App for books, genres, authors
├── cart/                    # App for cart functionality
├── media/                   # Uploaded images (book covers, author photos)
└── requirements.txt
📮 API Endpoints Overview
Method	Endpoint	Description
GET	/api/books/	List all books
POST	/api/books/	Add a new book
GET	/api/genres/	List all genres
GET	/api/authors/	List all authors
GET	/api/cart/	View user cart
POST	/api/cart/add/	Add item to cart
POST	/api/cart/remove/	Remove item from cart
Note: Endpoint paths may vary depending on your URL configuration.

📸 Media Uploads
Make sure your MEDIA_URL and MEDIA_ROOT are correctly set in settings.py. During development, serve media files like this:

python
Copy
Edit
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
🧪 Optional: API Testing with Postman
You can import the API collection into Postman or use tools like httpie or curl for testing.

🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

📄 License
This project is open-source and available under the MIT License.

vbnet
Copy
Edit

Let me know if you're using any extras like **DRF SimpleJWT**, **Cloudinary**, or **Docker**, and I can update this README to include those!






