# 👁️ AI Face Recognition Attendance System

An intelligent attendance system that uses **Face Recognition (YOLO + FaceNet)** to automatically detect and mark attendance in real time.

---

## 🚀 Features

* 🔐 Admin login system
* 👤 User registration with face capture
* ⏳ Admin approval workflow (Approve / Reject users)
* 📷 Real-time face detection using YOLOv8
* 🧠 Face recognition using FaceNet embeddings
* 🕒 Automatic attendance marking (Check-in / Check-out)
* 📊 Dashboard with analytics and insights
* 📧 Email notifications for approval & attendance

---

## 🧠 Tech Stack

* **Frontend**: Streamlit
* **Backend**: Python
* **Database**: SQL Server (pyodbc)
* **Computer Vision**: OpenCV, YOLOv8
* **Deep Learning**: FaceNet (facenet-pytorch)
* **Others**: NumPy, Pandas

---

## 📂 Project Structure

```
Smart_Attendance/
│── app.py
│── requirements.txt
│
├── components/      # UI elements (navbar, sidebar, cards)
├── database/        # DB connection & queries
├── modules/         # Core logic (attendance, auth, recognition)
├── services/        # Email service
├── utils/           # Helpers & validators
├── views/           # Pages (dashboard, admin panel, analytics)
├── static/          # Images / assets
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```
git clone https://github.com/maniac-24/AI-Face-Recognition-Attendance-System.git
cd AI-Face-Recognition-Attendance-System
```

---

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 3️⃣ Setup Secrets

Create file: `.streamlit/secrets.toml`

```
[email]
sender = "your_email@gmail.com"
password = "your_app_password"
```

---

### 4️⃣ Run Application

```
streamlit run app.py
```

---

## 📸 Screenshots



---

## 🔮 Future Improvements

* Multi-user authentication system
* Cloud deployment (Streamlit Cloud / AWS)
* Mobile-friendly UI
* Live notifications system

---

## 👨‍💻 Author

**Prashanth M**
Gmail: prashanthmadival64@gmail.com

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
