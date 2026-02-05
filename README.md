#  Library Management System (Django Web Application)

A full-featured **Library Management System** built with **Django**, designed to manage users, books, and authentication efficiently. The application includes **Google Sign-Up / Login**, role-based dashboards (admin & users), and a clean, modern UI.

This project was developed as part of an **Advanced Programming** academic course and is currently configured in a **testing (development) environment**, particularly regarding Google authentication.

---

##  Features

* User authentication (Login / Register)
* **Google Sign-Up & Login (OAuth 2.0 – Test Mode)**
* Role-based access (Admin / User)
* User profile management
* Admin dashboard for managing users
* Secure authentication flow
* Clean UI with Bootstrap 5

---

##  Technologies Used

### Backend

* **Python 3.x**
* **Django**
* **Django REST Framework (API development)**

### Authentication

* **django-allauth** (Google OAuth)
* **social-auth-app-django**
* **cryptography** (security & encryption support)

### Frontend

* HTML5 / CSS3 / JS
* Bootstrap 5
* Font Awesome

### Database

* SQLite (default Django database)

---

##  Python Dependencies

Install all required dependencies using the following command:

```bash
python -m pip install cryptography Django djangorestframework django-allauth social-auth-app-django
```

---

##  requirements.txt

Created a file named **requirements.txt** and added the requirements to be able to
 install everything at once:

```bash
pip install -r requirements.txt
```

---

##  Google Sign-Up & Sign-In (Test Environment)

### Important Notice (Please Read)

Google authentication in this project is configured under a **Google OAuth testing environment**, not a production environment.

This means:

* The application is **not publicly accessible** to all Google users
* Only a **limited number of test users** are allowed to authenticate
* Google requires explicit configuration using a **Client ID** and **Client Secret**

Because of this:

* The OAuth credentials **cannot be hardcoded** in the repository
* **GitHub blocks pushing sensitive credentials** for security reasons
* Each user cloning the project must manually configure Google credentials locally

This behavior is expected and normal for projects in development or academic testing phases.

---

##  Google Authentication Setup Steps

To enable **Google Sign-Up / Sign-In**, follow the steps below carefully.

### Step 1: Clone the Repository

```bash
git clone <repository-url>
```

---

### Step 2: Navigate to the Project Folder

```bash
cd Desktop
cd <cloned-project-folder>
cd ADVANCED-PROGRAMMING
```

---

### Step 3: Create the Configuration File

Run the following command:

```bash
copy config.example.py config.py
```

This file is intentionally excluded from version control to protect sensitive credentials.

---

### Step 4: Add Google OAuth Credentials

Open **config.py** and add the following test credentials:

```python
GOOGLE_CLIENT_ID = "83062460220-4okgb90b02filofc52v0h6fqj062u8go.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
```

Save the file.

> ⚠️ These credentials are provided **only for testing and academic evaluation purposes**.

---


---

### Step 5: Start the Development Server

```bash
python manage.py runserver
```

Open your browser and go to:

```
http://127.0.0.1:8000/
```
---


##  User Flow

* Users can register using email/password or Google
* Google accounts are linked automatically to Django users
* Only authorized test users can sign in via Google
* Admin users manage accounts through the dashboard

---

##  Notes

* This project uses **SQLite** by default
* Google OAuth runs in **test mode**, not production
* Credential isolation follows security best practices
* Designed for academic evaluation and demonstration purposes

---

##  Author

Developed as part of an **Advanced Programming** academic project.

---


## - Project Team:
Project developed by:

Lilia KAMIRI.

Nesrine TAIEB BENABBES.

Anfal BOUCHAREB.


