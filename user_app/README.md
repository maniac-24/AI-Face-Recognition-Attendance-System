# 👤 User Portal – AI Face Recognition Attendance System

The **User Portal** allows users to register, check approval status, and mark attendance using real-time face recognition.

---

## 🚀 Features

* 📝 **User Registration**

  * Enter details (name, email, phone, DOB)
  * Capture face using webcam
  * Store face embeddings securely

* ⏳ **Approval Status Tracking**

  * Check if account is **Pending / Approved / Rejected**
  * View rejection reason (if any)

* 📷 **Face-Based Attendance**

  * Real-time face detection using YOLOv8
  * Face recognition using FaceNet embeddings
  * Automatic attendance marking

* 🕒 **Attendance System**

  * First scan → ✅ Check-in
  * Second scan → 👋 Check-out
  * Prevents duplicate entries

* 🖼️ **Live Camera Preview**

  * Shows captured face image
  * Displays recognition result with confidence (distance)

---

## 🧠 Tech Stack

* **Frontend**: Streamlit
* **Backend**: Python
* **Database**: SQL Server (pyodbc)
* **Computer Vision**: OpenCV, YOLOv8
* **Deep Learning**: FaceNet (facenet-pytorch)
* **Others**: NumPy

---

## 📂 Folder Structure

```id="q7rj3z"
user_app/
│── app.py                 # Entry point
│── requirements.txt
│
├── database/              # DB connection & models
├── modules/               # Face recognition & attendance logic
├── utils/                 # Helpers & validators
├── views/                 # Pages (register, status, attendance)
├── static/                # Assets
```

---

## ⚙️ How to Run User Portal

### 1️⃣ Navigate to user_app

```id="bbh8o7"
cd user_app
```

### 2️⃣ Install dependencies

```id="b5q3kq"
pip install -r requirements.txt
```

### 3️⃣ Run the app

```id="nyrs1g"
streamlit run app.py
```

---

## 🔄 User Workflow

1. User registers with personal details + face capture
2. Admin reviews and approves the account
3. User checks approval status
4. After approval, user can mark attendance
5. System automatically records check-in and check-out

---

## 📸 Screenshots

(Add screenshots here)

---

## ⚠️ Notes

* Only **approved users** can mark attendance
* Ensure camera access is enabled
* Good lighting improves recognition accuracy
* Face should be clearly visible during capture

---

## 🚀 Future Enhancements

* Multi-face detection support
* Mobile camera integration
* Improved accuracy with multiple embeddings
* Real-time notifications

---

## 👨‍💻 Author

**Prashanth M**
Gmail: [prashanthmadival64@gmail.com](mailto:prashanthmadival64@gmail.com)

---
