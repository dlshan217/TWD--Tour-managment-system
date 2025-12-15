# TWD — Travel & Tour Management System

TWD is a full-stack **Django-based travel booking platform** that allows users to browse approved tour packages, book trips, make payments, and manage profiles.  
Vendors can register, create tour packages, and manage bookings — all with a clean, modern UI.

---

##  Features

###  User Features
- User signup & login (secure hashed passwords)
- View **only admin-approved packages**
- Book packages with pre-filled user details
- Razorpay payment integration
- View own booking history
- User profile page

---

###  Vendor Features
- Vendor signup & login (password hashed)
- Create, update, delete tour packages
- Upload package images
- View all bookings made on their packages
- Vendor profile displayed in vendor dashboard

---

###  Admin (Django Admin Panel)
- Approve or reject tour packages  
- Manage users, vendors, packages, bookings  
- Admin approval required for packages to appear to users

---

##  Tech Stack

| Component | Technology |
|----------|------------|
| Backend | **Python-Django ** |
| Frontend | HTML, CSS, custom UI |
| Database | SQLite (default) |
| Authentication | Session-based |
| Payment | Razorpay integration |
|  |  |
