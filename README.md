# Blog Application API

This is the backend API for a full-stack blogging application, built using **Django** and **Django REST Framework (DRF)**. It provides a RESTful API to handle blog posts, user authentication, and other core functionalities of the blog.

**Live API URL**: [https://inkspire-api.onrender.com](https://inkspire-api.onrender.com)

---

## Features

- **User Authentication**: Allows user registration, login, and token-based authentication (using JWT).
- **Blog Post Management**: Users can create, update, delete, and view blog posts.
- **CRUD Operations**: All functionalities (Create, Read, Update, Delete) are available for blog posts and comments.
  
---

## Tech Stack

- **Backend Framework**: Django
- **API Framework**: DRF
- **Authentication**: JWT (JSON Web Token)
- **Database**: SQLite

---

## Installation

Follow these steps to set up the project locally:

### Prerequisites

- Python >= 3.8
- pip (Python package manager)
- Virtual environment (recommended)

### 1. Clone the repository

```bash
git clone https://github.com/username/blog-application-api.git
cd blog-application-api
```

### 2. Create a virtual environment (Optional but recommended)
```
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Run the build script
```
./build.sh
