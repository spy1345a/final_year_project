# 💰 Expense Tracker

> An intelligent expense tracking application with AI-powered categorization and a modern web interface.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## ✨ Features

- **🔐 User Authentication** - Secure signup/login with JWT tokens
- **💸 Expense Management** - Add, view, and delete expenses
- **🤖 AI Categorization** - Automatic expense categorization using ML
- **📊 Dashboard** - Visual breakdown of expenses with charts
- **📥 Import/Export** - Bulk import expenses from CSV files
- **👤 User Roles** - Admin and regular user roles
- **🗑️ Admin Controls** - Delete all expenses across users

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/spy1345a/final_year_project.git
cd final_year_project

# Start the application (auto-installs dependencies)
python3 start.py
```

That's it! The application will:
1. Create `.env` configuration file
2. Set up virtual environment
3. Install dependencies
4. Start both servers

---

## 🌐 Access Points

| Service | URL |
|---------|-----|
| **Web Application** | http://localhost:5000 |
| **API (FastAPI)** | http://localhost:8000 |
| **API Documentation** | http://localhost:8000/docs |

---

## 🔑 Default Admin Credentials

| Field | Value |
|-------|-------|
| Username | `admin` |
| Password | `Blabla24a1` |

> ⚠️ **Important:** Change the default admin password in `.env` file before deploying!

---

## 📁 Project Structure

```
final_year_project/
├── api/
│   └── main.py          # FastAPI backend
├── web_application/
│   ├── flask_app.py     # Flask web server
│   ├── templates/       # HTML templates
│   └── static/          # CSS, JS, images
├── ai_intratation/
│   └── ai_main.py       # ML model for categorization
├── .env                 # Configuration (auto-generated)
├── .env.example         # Example configuration
├── requirements.txt     # Python dependencies
└── start.py            # Application launcher
```

---

## 🔧 Configuration

Edit the `.env` file to customize settings:

```env
# Flask Configuration
FASTAPI_URL=http://127.0.0.1:8000
FLASK_SECRET_KEY=your-secret-key
DEBUG=true

# FastAPI Configuration
SECRET_KEY=your-jwt-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=users.db

# Default Admin User
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-password
```

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/signup` | Register new user |
| POST | `/login` | Login and get JWT token |
| GET | `/profile` | Get user profile |

### Expenses
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/expenses` | Add new expense |
| GET | `/expenses/recent` | Get recent expenses |
| DELETE | `/expenses/{id}` | Delete expense |
| DELETE | `/expenses/delete-all` | Delete all (admin only) |
| POST | `/expenses/import` | Import from CSV |

### AI
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/predict` | Categorize expense text |

---

## 🛠️ Manual Setup (Optional)

If you prefer to run services manually:

```bash
# Create virtual environment
python3 -m venv .venv

# Activate environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Start API
uvicorn api.main:app --host 0.0.0.0 --port 8000

# Start Web (in new terminal)
python web_application/flask_app.py
```

---

## 📝 License

This project is for educational purposes as part of BCA final year project.

---

## 👨‍💻 Author

**Final Year Project** - BCA

---

<p align="center">
  Made with ❤️ for educational purposes
</p>
