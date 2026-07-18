# 🔐 Secure Password Generator & Vault

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production-success)
![Version](https://img.shields.io/badge/Version-6.0%20Professional-orange)

A modern Password Generator and Password Vault application built with **Python**, **Streamlit**, **SQLite**, **Cryptography**, **Plotly**, **Pandas**, and **zxcvbn**.

The application helps users generate secure passwords, evaluate password strength, securely store credentials using encryption, monitor password health, visualize analytics, and manage passwords through an encrypted vault.

---

# ✨ Features

## 🔑 Password Generator

- Generate secure random passwords
- Custom password length
- Uppercase letters
- Lowercase letters
- Numbers
- Symbols
- Exclude similar characters
- Custom character exclusion
- Multiple password generation
- Password templates
- Password categories

---

## 🔐 Password Vault

- Master Password Authentication
- Recovery Key
- Security Questions
- Secure Password Encryption
- Password Categories
- Password Tags
- Secure Notes
- Search Passwords
- Favorite Passwords
- Password Expiry
- Edit Password
- Delete Password
- Auto Lock
- Dashboard

---

## 📊 Password Analytics

- Password Statistics
- Password Strength
- Entropy Calculator
- Crack Time Estimation
- Health Report
- Password Recommendations
- Interactive Charts
- Vault Analytics

---

## 🛡 Security Features

- Fernet Encryption
- PBKDF2 Password Hashing
- Local Breach Detection
- Password History
- Password Expiry
- Login Attempt Protection
- Recovery Verification
- Secure Storage
- Encryption Key Management

---

## 📤 Export Features

- CSV Export
- JSON Export
- Vault Backup
- Master Backup
- Analytics Report

---

# 📸 Screenshots

## Home

![Home](assets/screenshots/home.png)

## Password Generator

![Generator](assets/screenshots/generator.png)

## Password Vault

![Vault](assets/screenshots/vault.png)

## Analytics Dashboard

![Analytics](assets/screenshots/dashboard.png)

## Password Health

![Health](assets/screenshots/health-report.png)

## History

![History](assets/screenshots/history.png)

---

# 🏗 Project Structure

```text
Secure-Password-Generator-Vault
│
├── .streamlit/
│
├── assets/
│   ├── banner.png
│   ├── favicon.png
│   ├── logo.png
│   └── screenshots/
│
├── data/
│
├── analytics.py
├── app.py
├── breach.py
├── category.py
├── clipboard.py
├── cracktime.py
├── crypto.py
├── database.py
├── entropy.py
├── generator.py
├── health.py
├── history.py
├── master.py
├── recommend.py
├── score.py
├── session.py
├── sidebar.py
├── stats.py
├── strength.py
├── tags.py
├── templates.py
├── ui.py
├── vault.py
│
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

# ⚙ Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Core Programming |
| Streamlit | User Interface |
| SQLite | Local Database |
| Cryptography | Encryption |
| Plotly | Analytics Charts |
| Pandas | Data Processing |
| zxcvbn | Password Strength |
| Pyperclip | Clipboard |

---

# 🔒 Security Architecture

### Password Encryption

- Fernet Encryption
- Secure Key Management

### Master Password

- PBKDF2-HMAC-SHA256
- Salted Password Hashing
- Password History
- Password Expiry
- Failed Login Protection

### Recovery

- Recovery Key
- Security Questions
- Password Reset

---

# 🚀 Installation

Clone repository

```bash
git clone https://github.com/d2oshahnawaz/Secure-Password-Generator-Vault.git
```

Move into project

```bash
cd Secure-Password-Generator-Vault
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run application

```bash
streamlit run app.py
```

---

# ☁ Streamlit Deployment

Push your project to GitHub.

Deploy on Streamlit Community Cloud.

Repository:

```
Secure-Password-Generator-Vault
```

Main file

```
app.py
```

Python Version

```
3.10+
```

---

# 📦 Requirements

- Python 3.10+
- Streamlit
- Pandas
- Plotly
- Cryptography
- zxcvbn
- openpyxl

Install

```bash
pip install -r requirements.txt
```

---

# 📈 Current Modules

| Module | Status |
|---------|:------:|
| Password Generator | ✅ |
| Password Vault | ✅ |
| Master Password | ✅ |
| Recovery Key | ✅ |
| Security Questions | ✅ |
| Encryption | ✅ |
| Password History | ✅ |
| Analytics Dashboard | ✅ |
| Password Health | ✅ |
| Export CSV | ✅ |
| Export JSON | ✅ |
| Favorites | ✅ |
| Categories | ✅ |
| Search | ✅ |
| Auto Lock | ✅ |

---

# 🎯 Future Roadmap

- Two-Factor Authentication
- Browser Extension
- Cloud Synchronization
- Multi User Support
- Password Sharing
- Mobile Application
- API Support
- PDF Export
- Dark/Light Themes
- Password Reuse Detection

---

# ⚠ Disclaimer

This project is intended for educational, research, and personal use.

Users are responsible for securely storing their Recovery Key and Master Password.

---

# 🤝 Contributing

Contributions are welcome.

1. Fork Repository

2. Create Branch

```bash
git checkout -b feature-name
```

3. Commit

```bash
git commit -m "Add feature"
```

4. Push

```bash
git push origin feature-name
```

5. Open Pull Request

---

# 👨‍💻 Author

**Mohd Shahnawaz**

Founder & CEO — Tech Education World™

GitHub

https://github.com/d2oshahnawaz

LinkedIn

https://www.linkedin.com/in/mohd-shahnawaz-645371205/

---

# ⭐ Support

If you like this project,

⭐ Star this repository.

🐞 Report bugs.

💡 Suggest improvements.

🤝 Contribute to development.

---

# 📄 License

This project is licensed under the **MIT License**.

See the LICENSE file for details.

---

## Version

**Secure Password Generator & Vault**

**Version 6.0 Professional**

Built with ❤️ using Python & Streamlit.
