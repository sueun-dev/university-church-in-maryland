# University Church in Maryland Official Website

**Live Site**: [https://www.uchurchmd.org/](https://www.uchurchmd.org/)  
[![License](https://img.shields.io/badge/License-Proprietary-blue.svg)](LICENSE)

---

## 🌟 Highlights  
- **Modern Dependency Management**: Fully powered by Poetry for seamless package handling.  
- **Production-Ready Architecture**: Deployed on GCP Compute Engine with HTTPS/SSL.  
- **Security First**: Rate-limited authentication, encrypted file uploads, and IP blocking.  

---

## 🛠 Tech Stack  
**Backend**: Flask (Python 3.10+) | **Database**: PostgreSQL  
**Frontend**: HTML5, CSS3, Vanilla JS | **Infra**: GCP Compute Engine, Nginx, Certbot  

---

## 🚀 Quick Start with Poetry  

### 1. Clone & Install  
```shell
git clone https://github.com/sueun-dev/university-church-in-maryland.git
cd official-website
poetry install  # Installs all dependencies  
```

### 2. Configure Environment  
Create a `.env` file in the root directory:
```env
DATABASE_URL="postgresql://user:password@localhost:5432/kusa_db"
SECRET_KEY="your-random-secret-key"  # Used for Flask session encryption
```

### 3. Run the App  
```shell
poetry shell    # Activates the virtual environment
python run.py   # Starts the Flask dev server
```

---

## 🔒 Security Features  
- **Brute-Force Protection**: Blocks IPs after 5 failed login attempts (24-hour cooldown).  
- **File Upload Safeguards**:  
  - Configurable size limits via `MAX_FILE_SIZE` in `.env`.  
  - Virus scanning for uploaded files (optional GCP integration).  

---

## ☁️ Deployment Guide  
1. **GCP Compute Engine Setup**:  
   - Ubuntu 22.04 LTS instance with firewall rules allowing HTTPS/HTTP.  
2. **HTTPS Configuration**:   
   ```shell
   sudo certbot --nginx -d umdkusa.com -d www.umdkusa.com
   ```
3. **Run as Background Service**:  
   ```shell
   nohup poetry run python run.py &  # Persistent execution
   ```

---

## 📜 License  
Free to use

---

## Developer
**Developer**: Sueun Cho

**E-mail**:  sueun.dev@gmail.com

**LinkedIn**: [LinkedIn](https://www.linkedin.com/in/sueun-cho-625262252/)

---

_Last Updated: February 05, 2025_

