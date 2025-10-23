# 🐍 Django Piscine — Portfolio Edition

### 🌍 Overview
A practical and comprehensive journey through Python and Django development — from foundational coding to building full-stack web applications with authentication, ORM, and optimized data structures.

---

## 🧠 Core Skills
- Django app architecture and modular design  
- ORM performance tuning & N+1 query prevention  
- User authentication, authorization, and sessions  
- Internationalization (i18n) and localization  
- Class-based and generic views  
- REST mindset and API integration  
- SQL & PostgreSQL fundamentals  
- Bootstrap integration and responsive UI  

---

## ⚙️ Stack
**Languages:** Python 3.10+  
**Framework:** Django (LTS)  
**Database:** PostgreSQL  
**Frontend:** HTML, CSS, Bootstrap  
**Libraries:** Requests, BeautifulSoup, psycopg2, gettext  
**Tools:** pip, virtualenv, bash scripting  

---

## 📘 Modules Overview

### 🪜 Django - 0 Initiation
Introduced core Python concepts: variables, data structures, and file handling. Learned to build small automation scripts and manage environments.

### 📚 Django - 1 Libraries
Built API-based utilities and learned dependency management. Highlights include:
- **Geohashing algorithm** implementation.  
- Automated package installation using pip and shell scripting.  
- Wikipedia content retrieval via **Requests**, **dewiki**, and **BeautifulSoup**.  
→ Real-world experience in API consumption, data cleaning, and automation.

### 🧩 Django - 1 BaseDjango
First Django project setup with modular structure.  
- Implemented routing, templates, static files, and navigation bars.  
- Practiced **DRY** via `base.html` inheritance.  
- Worked with simple forms and request/response cycle.

### 🧱 Django - 2 ORM
Focused on persistence, database modeling, and performance.  
- Designed relational models and migrations using Django ORM.  
- Used `psycopg2` for raw SQL control.  
- Practiced insertions, deletions, joins, and filtering.  
- Identified and solved **N+1 queries** with `select_related()` and `prefetch_related()`.  
→ Hands-on understanding of ORM vs SQL and backend efficiency.

### 🧠 Django - 3 Advanced
Developed a production-style content platform with **Articles** and **UserFavorites** models.  
- Used **Generic Class-Based Views** for scalable design.  
- Implemented **authentication & authorization** workflows.  
- Added **i18n/globalization** support for multilingual content.  
- Practiced clean URL management and relational data modeling.

### 🔐 Django - 3 Sessions
Explored user sessions and interactive interfaces.  
- Built session-based anonymous user handling (42-second identity).  
- Added login, signup, and logout logic using Django’s auth system.  
- Created a **Tips system** with voting, moderation, and Bootstrap UI.  
→ Learned state management, UX-driven logic, and secure data flow.

---

## 🚀 Run It Yourself
```bash
git clone https://github.com/agvangrigoryan/django_piscine.git
cd django_piscine/3-advanced
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 🎯 Outcome
Mastered the development of scalable Django applications — combining **backend data modeling**, **auth and sessions**, **ORM optimization**, and **clean UI integration**.  
This repository represents not just technical fluency, but an understanding of **real-world backend architecture and maintainable project design**.
