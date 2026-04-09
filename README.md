# 🍠 SweetRoots — Roots on Route 66

A community-powered sweet potato plant tracking web application that allows users to track plant lineage, take clippings, and share their growing journey.

---

## 📖 About

SweetRoots was built for the **Tulsa Farmers Market** community to track sweet potato plants and their clipping lineage. Users can get a clipping from a mother plant, grow it, take clippings from it, and track the entire family tree of any plant back to its original source. Plants can be created anonymously or linked to a registered user account.

---

## ✨ Features

- 🌱 **Plant Tracking** — Add, update, and delete sweet potato plants
- 👨‍👦 **Lineage Tracking** — Track parent/child relationships between plants through clippings
- 📊 **Generation Tracking** — Automatically calculates plant generation from its lineage
- 🌿 **Growth Status** — Update plant status (Propagating, Growing, Flowering, Harvesting, Harvested)
- 👤 **User Accounts** — Register, login, and manage your profile
- 📸 **Profile Pictures** — Upload profile photos via Cloudinary
- 🔍 **Search** — Search your garden by plant name, status, or parent ID
- 📱 **QR Code Support** — Plants can be shared via QR code containing the plant URL
- 🖼️ **Community Gallery** — Share photos and videos of your plants
- 📥 **Data Export** — Export your garden data as JSON
- 🌙 **Dark Mode** — Automatically adapts to system preference
- 📱 **Mobile Responsive** — Works on all screen sizes

---

## 🛠️ Tech Stack

### Frontend

- HTML, CSS, JavaScript (Vanilla)
- Font Awesome icons
- AOS (Animate On Scroll)
- Google Fonts (Inter, Playfair Display)

### Backend

- Python 3.10
- FastAPI
- Motor (async MongoDB driver)
- MongoDB (local)
- Pydantic v2
- bcrypt (password hashing)
- Cloudinary (image uploads)
- Python-dotenv

---

## 📁 Project Structure

```
roots-on-route-66/
├── frontend/
│   ├── sweetpotatoes.html
│   ├── style.css
│   └── script.js
├── backend/
│   └── app/
│       ├── main.py
│       ├── config/
│       │   └── mongodb.py
│       ├── models/
│       │   ├── user.py
│       │   └── plant.py
│       ├── schemas/
│       │   ├── user.py
│       │   └── plant.py
│       ├── services/
│       │   ├── user_service.py
│       │   ├── plant_service.py
│       │   └── cloudinary_service.py
│       ├── routes/
│       │   ├── users.py
│       │   └── plants.py
│       └── utils/
│           └── cloudinary.py
├── requirements.txt
└── .env
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10
- MongoDB installed locally
- WSL (Windows Subsystem for Linux) if on Windows
- A Cloudinary account (for profile picture uploads)

### 1. Clone the repo

```bash
git clone https://github.com/your-username/roots-on-route-66.git
cd roots-on-route-66
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Create your `.env` file

Create a `.env` file inside the `backend/` folder:

```
MONGODB_URI=mongodb://localhost:27017
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
CLOUDINARY_UPLOAD_PRESET=your_upload_preset
```

### 5. Start MongoDB

```bash
sudo service mongod start
```

### 6. Start the backend

```bash
cd backend
uvicorn app.main:app --reload --port 8001
```

### 7. Open the frontend

Open `frontend/sweetpotatoes.html` directly in your browser or use the Live Server extension in VSCode.

---

## 📡 API Routes

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/` | Register a new user |
| POST | `/users/login` | Login |
| GET | `/users/{user_id}` | Get user by ID |
| PUT | `/users/{user_id}` | Update user |
| PUT | `/users/{user_id}/password` | Change password |
| DELETE | `/users/{user_id}` | Delete user |
| GET | `/users/{user_id}/plants` | Get all plants for a user |
| POST | `/users/{user_id}/profile-picture` | Upload profile picture |

### Plants

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/plants/` | Create a plant |
| GET | `/plants/{plant_id}` | Get plant by ID |
| PUT | `/plants/{plant_id}` | Update plant |
| DELETE | `/plants/{plant_id}` | Delete plant |
| POST | `/plants/{plant_id}/clipping` | Take a clipping from a plant |
| POST | `/plants/{plant_id}/claim` | Claim an anonymous plant |
| GET | `/plants/{plant_id}/lineage` | Get full lineage of a plant |

---

## 🌱 How Plant Lineage Works

```
Original Plant (Generation 0)
        ↓
  Clipping taken → Child Plant (Generation 1)
        ↓
  Clipping taken → Child Plant (Generation 2)
```

Every plant stores a `parentPlantId` linking it to the plant it was clipped from. The `GET /plants/{plant_id}/lineage` endpoint traces all the way back to the original plant. Generation is automatically calculated when a clipping is created.

---

## 🔒 Security Notes

- Passwords are hashed with bcrypt — never stored in plain text
- CORS is currently open for development — restrict to your frontend URL before deploying
- JWT authentication is not yet implemented — planned for a future release
- Profile pictures are stored on Cloudinary — never on the server

---

## 🗺️ Roadmap

- [ ] JWT authentication
- [ ] Admin dashboard
- [ ] QR code generation per plant
- [ ] Progress notes and media per plant stored in MongoDB
- [ ] Community gallery backed by database
- [ ] Plant care calendar
- [ ] Deploy to production

---

## 🏴‍☠️ Made with ❤️ for the Tulsa Farmers Market community
