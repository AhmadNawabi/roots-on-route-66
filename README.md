# 🌱 Roots on Route 66

## 📌 Overview

**Roots on Route 66** is a QR-powered community propagation platform that allows users to:

- Scan a QR code to learn how to grow sweet potatoes
- Optionally sign up to receive a free plant clipping
- Track their plant and its origin (mother plant)
- Log progress and contribute to a growing network

---

## 🎯 MVP Goals

The goal of the MVP is to:

- Provide a simple QR → landing experience
- Allow optional user registration
- Assign a plant to registered users
- Track plant data and parent relationships
- Allow users to log progress

---

## 🧱 Tech Stack

### Backend
- Python
- FastAPI
- MongoDB Atlas

### Frontend
- Next.js

### Media Storage
- Cloudinary

### Deployment (later phase)
- Docker
- Google Cloud Run

---
### Main Project Structure
roots-on-route-66/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config/
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── user_model.py
│   │   │   ├── plant_model.py
│   │   │   └── log_model.py
│   │   ├── schemas/
│   │   │   ├── user_schema.py
│   │   │   ├── plant_schema.py
│   │   │   └── log_schema.py
│   │   ├── routes/
│   │   │   ├── user_routes.py
│   │   │   ├── plant_routes.py
│   │   │   ├── qr_routes.py
│   │   │   └── log_routes.py
│   │   ├── services/
│   │   │   ├── user_service.py
│   │   │   ├── plant_service.py
│   │   │   ├── qr_service.py
│   │   │   └── log_service.py
│   │   └── utils/
│   │       └── cloudinary.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx
│   │   │   ├── qr/[code]/page.tsx
│   │   │   ├── register/page.tsx
│   │   │   └── plant/[id]/page.tsx
│   │   ├── components/
│   │   │   ├── RegisterForm.tsx
│   │   │   ├── PlantView.tsx
│   │   │   └── QRInfo.tsx
│   │   └── lib/
│   │       └── api.ts
│   ├── package.json
│   └── README.md
│
├── .gitignore
└── README.md
