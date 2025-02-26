# SmartRoute 🚗🛣️  

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)  
[![Flask](https://img.shields.io/badge/Flask-Backend-orange.svg)](https://flask.palletsprojects.com/)  

SmartRoute is a **Flask-based web application** designed for optimized trip routing. It provides an interactive interface for users to find the best routes with a visual representation of paths.  

---

## 🚀 Features  
✅ **Flask Backend** for processing routes and map visualization.  
✅ **Optimized Trip Mapping** with path rendering in HTML.  
✅ **Lightweight and Fast** for easy deployment and execution.  

---

## 📦 Installation & Setup  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/Shamik200/SmartRoute.git
cd SmartRoute
```  

### 2️⃣ Create and Activate Python Environment  
```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```  

### 3️⃣ Install Dependencies & Run Server  
```bash
pip install -r requirements.txt
python app.py
```  

---

## 📡 API Usage  
- **GET /**: Loads the homepage with the route search interface.  
- **POST /find-route**: Accepts user input and returns optimized routes.  

---

## 📂 Project Structure  
```
📂 SmartRoute
 ┣ 📂 Images/                           # Screenshots & assets
 ┣ 📜 README.md                         # Project details
 ┣ 📜 app.py                             # Flask backend
 ┣ 📜 optimized_trip_map_with_paths_return.html  # Route visualization page
 ┣ 📜 requirements.txt                   # Dependencies
 ┣ 📜 runtime.txt                         # Runtime configuration
 ┣ 📜 wsgi.py                             # WSGI entry point
```  

---

## 🛠 Built With  
- **Python** (3.8+)  
- **Flask** (for backend logic)  
- **HTML, CSS, JavaScript** (for frontend)  

---

🚀 **Made by [Shamik](https://github.com/Shamik200)**  
