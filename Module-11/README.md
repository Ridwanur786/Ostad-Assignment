# Property Rental & Management System - Authentication App

**Ostad Django Batch 12 - Module 11 Assignment**

This project implements a complete, role-based User Authentication and Profile Management System using Django 6 and Bootstrap 5.

---

## 🌟 Key Features

### 1. User Registration (`/register/`)
- Choose between two distinct user roles:
  - **Property Owner**: Allowed to create and manage properties, review rental requests.
  - **Tenant**: Allowed to browse, search, send rental requests, and submit reviews.
- Fields: Username, Email, First Name, Last Name, Phone Number, Address, Profile Picture, and Password.
- Automatic password validation and uniqueness checks for username and email.
- Instant automatic login upon successful registration.

### 2. User Login (`/login/`)
- Flexible login: sign in with either your **Username** or **Email address**.
- **Remember Me** functionality to control session expiration.
- Show/Hide password toggle for better user experience.

### 3. User Logout (`/logout/`)
- Session-safe logout supporting both GET and POST.
- Redirects with clear feedback notifications.

### 4. Profile Dashboard & Update (`/profile/` & `/profile/edit/`)
- **Profile Overview**: Displays user avatar, full name, role badge, contact details, join date, and role permissions.
- **Profile Update**: Edit first name, last name, email address, phone number, address, role, and upload custom profile pictures with live preview.
- **Change Password**: Secure password update without losing the active session.

### 5. Django Admin (`/admin/`)
- Custom `UserAdmin` with an inline `Profile` view.
- Dedicated `ProfileAdmin` with filters by role and search by username, email, phone, and address.

---

## 📁 Project Structure

```text
Module-11/
│
├── ecom-env/                    # Virtual environment
├── rental_system/               # Project configuration
│   ├── settings.py              # App, static, media, template settings
│   ├── urls.py                  # Root URL configuration
│   ├── wsgi.py
│   └── asgi.py
│
├── authentication/              # Authentication app
│   ├── models.py                # Profile model with post_save signal
│   ├── forms.py                 # Registration, Login, User & Profile Update forms
│   ├── views.py                 # Register, Login, Logout, Profile, Change Password views
│   ├── urls.py                  # Authentication routing
│   ├── admin.py                 # User & Profile admin configuration
│   └── tests.py                 # Automated unit tests
│
├── templates/                   # HTML Templates (Bootstrap 5)
│   ├── base.html                # Base layout with navbar, alerts & footer
│   ├── home.html                # Landing page showcasing the rental system
│   └── authentication/
│       ├── register.html        # Registration with role cards
│       ├── login.html           # Login with username/email & toggle password
│       ├── profile.html         # User profile dashboard
│       ├── profile_update.html  # Profile editing with image preview
│       └── change_password.html # Password change page
│
├── static/                      # Static assets (CSS/JS)
│   └── css/style.css
├── media/                       # Uploaded profile pictures
├── manage.py                    # Django management script
├── requirements.txt             # Project dependencies
└── README.md
```

---

## 🚀 How to Run the Project

1. **Activate the Virtual Environment**:
   - In PowerShell:
     ```powershell
     .\ecom-env\Scripts\Activate.ps1
     ```
   - In Command Prompt:
     ```cmd
     .\ecom-env\Scripts\activate.bat
     ```

2. **Run Migrations** (already applied):
   ```bash
   python manage.py migrate
   ```

3. **Create a Superuser** (optional, for `/admin/` access):
   ```bash
   python manage.py createsuperuser
   ```

4. **Start the Development Server**:
   ```bash
   python manage.py runserver
   ```

5. Open your browser and navigate to:
   - **Home**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - **Register**: [http://127.0.0.1:8000/register/](http://127.0.0.1:8000/register/)
   - **Login**: [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)
   - **Profile**: [http://127.0.0.1:8000/profile/](http://127.0.0.1:8000/profile/)
   - **Edit Profile**: [http://127.0.0.1:8000/profile/edit/](http://127.0.0.1:8000/profile/edit/)
   - **Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
