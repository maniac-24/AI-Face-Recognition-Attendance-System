# 🛠️ Admin Panel – AI Face Recognition Attendance System

The **Admin Panel** is responsible for managing users, monitoring attendance, and analyzing system data. It provides full control over the attendance system with approval workflows and insights.

---

## 🚀 Features

* 🔐 **Admin Authentication**

  * Secure login system for administrators

* 👤 **User Management**

  * View registered users
  * Approve or reject new registrations
  * Track user status (Pending / Approved / Rejected)

* 📊 **Dashboard & Analytics**

  * Total users, attendance stats
  * Daily / monthly attendance insights
  * Graphs and visual analytics

* 🕒 **Attendance Monitoring**

  * View all attendance records
  * Check-in / Check-out tracking
  * Status (Present / Absent / Half-day)

* 📧 **Email Notifications**

  * Send approval/rejection emails
  * Notify users about attendance updates

---

## 🧠 Tech Stack

* **Frontend**: Streamlit
* **Backend**: Python
* **Database**: SQL Server (pyodbc)
* **Visualization**: Pandas, Charts
* **Computer Vision**: OpenCV, YOLO, FaceNet

---

## 📂 Folder Structure

```
admin_app/
│── app.py                 # Entry point
│── requirements.txt
│
├── components/            # UI components (navbar, sidebar, cards)
├── database/              # DB connection & queries
├── modules/               # Core logic (auth, attendance, recognition)
├── services/              # Email service
├── utils/                 # Helpers & validators
├── views/                 # Pages (dashboard, analytics, admin panel)
├── static/                # Images / assets
```

---

## ⚙️ How to Run Admin Panel

### 1️⃣ Navigate to admin_app

```
cd admin_app
```

### 2️⃣ Install dependencies (if not already)

```
pip install -r requirements.txt
```

### 3️⃣ Run the app

```
streamlit run app.py
```

---

## 🔐 Admin Workflow

1. Admin logs into the system
2. Reviews newly registered users
3. Approves or rejects users
4. Monitors attendance records
5. Views analytics and reports

---

## 📌 Notes

* Only **approved users** can mark attendance
* Admin panel controls full system behavior
* Ensure database connection is properly configured

---

## 🚀 Future Enhancements

* Role-based access control
* Advanced analytics dashboard
* Export reports (CSV / PDF)
* Real-time alerts

---

## 👨‍💻 Author

**Prashanth M**
Gmail: [prashanthmadival64@gmail.com](mailto:prashanthmadival64@gmail.com)

---
