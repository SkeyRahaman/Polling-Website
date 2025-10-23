# 🗳️ Polling Service (Django REST Framework)

A modular, scalable Polling System API built using Django REST Framework (DRF).
This service allows users to create, manage, vote, and analyze polls.
It is designed as a standalone microservice that can integrate with external authentication and user services.

---

## 🚀 Features

- Polls CRUD — Create, update, delete, and retrieve polls with metadata.
- Options Management — Add or edit poll options dynamically.
- Voting System — Secure, idempotent voting mechanism (one vote per user per poll).
- Likes & Dislikes — Reactions system using PUT/DELETE semantics.
- Comments & Replies — Threaded comment system for each poll.
- Analytics — Aggregated poll results and detailed admin analytics.
- Moderation — Report and review abusive polls.
- Image Uploads — Upload images for polls (stored in object storage like S3).
- Microservice Ready — Integrates with external Auth and User Management APIs.
- Soft Delete — Polls are never permanently removed; safe recovery is possible.

---

## 🧱 Tech Stack

| Layer | Technology |
|--------|-------------|
| Backend Framework | Django REST Framework |
| Database | PostgreSQL |
| Containerization | Docker & Docker Compose |
| Authentication | External Auth Service via REST |
| Storage | S3 / MinIO (for images) |
| ORM | Django ORM |
| Caching / Async | Redis (optional for analytics and vote caching) |

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
bash git clone https://github.com/<your-username>/polling_service.git cd polling_service 

### 2️⃣ Create and Configure Environment

Create an .env file under env/polling_service/.env:
bash POSTGRES_USER=devuser POSTGRES_PASSWORD=devpassword POSTGRES_DB=polling_db DATABASE_URL=postgresql://devuser:devpassword@db:5432/polling_db  APP_ENV=development DEBUG=True SECRET_KEY=your_secret_key_here 

### 3️⃣ Build and Run with Docker
bash docker-compose up --build 

This starts:
- polling_service (Django app)
- polling_service_db (PostgreSQL database)

### 4️⃣ Apply Migrations
bash docker exec -it polling_service python manage.py migrate 

### 5️⃣ Access the API
- API Root: http://localhost:8002/api/
- Health Check: http://localhost:8002/health/

---

## 🧩 API Endpoints Overview

### 🗂️ Polls
| Method | Endpoint | Description |
|---------|-----------|-------------|
| POST | /polls | Create a new poll |
| GET | /polls | List all polls |
| GET | /polls/{id} | Retrieve poll details |
| GET | /polls/slug/{slug} | Lookup poll by slug |
| PATCH | /polls/{id} | Update poll details |
| DELETE | /polls/{id} | Soft delete a poll |

### ⚙️ Options
| Method | Endpoint | Description |
|---------|-----------|-------------|
| POST | /polls/{poll_id}/options | Add poll options |
| PATCH | /polls/{poll_id}/options/{option_id} | Edit an option |
| DELETE | /polls/{poll_id}/options/{option_id} | Remove an option |

### 🗳️ Voting & Reactions
| Method | Endpoint | Description |
|---------|-----------|-------------|
| POST | /polls/{poll_id}/vote | Cast a vote |
| DELETE | /polls/{poll_id}/vote | Remove user’s vote |
| PUT | /polls/{poll_id}/like | Like a poll |
| DELETE | /polls/{poll_id}/like | Remove like |
| PUT | /polls/{poll_id}/dislike | Dislike a poll |
| DELETE | /polls/{poll_id}/dislike | Remove dislike |

### 📊 Results & Analytics
| Method | Endpoint | Description |
|---------|-----------|-------------|
| GET | /polls/{poll_id}/results | Basic vote results |
| GET | /polls/{poll_id}/analytics | Advanced admin analytics |

### 💬 Comments
| Method | Endpoint | Description |
|---------|-----------|-------------|
| POST | /polls/{poll_id}/comments | Add a comment |
| GET | /polls/{poll_id}/comments | List comments |
| PATCH | /polls/{poll_id}/comments/{comment_id} | Edit comment |
| DELETE | /polls/{poll_id}/comments/{comment_id} | Delete comment |

### 🧑‍💼 Moderation
| Method | Endpoint | Description |
|---------|-----------|-------------|
| POST | /polls/{poll_id}/report | Report poll abuse |
| GET | /moderation/reports | Admin view reports |

### 🖼️ Image Upload
| Method | Endpoint | Description |
|---------|-----------|-------------|
| POST | /polls/{poll_id}/image | Upload image |
| DELETE | /polls/{poll_id}/image | Remove poll image |

### 🧮 Admin / Maintenance
| Method | Endpoint | Description |
|---------|-----------|-------------|
| GET | /polls/stats | Global poll statistics |
| POST | /polls/{id}/close | Force-close a poll |
| POST | /cleanup/expired-polls | Cleanup expired polls |

---

## 🧰 Project Structure
 polling_service/ ├─ app/ │ ├─ polls/ │ │ ├─ models/ │ │ ├─ serializers/ │ │ ├─ views/ │ │ ├─ urls.py │ │ └─ services/ │ ├─ comments/ │ ├─ analytics/ │ └─ moderation/ ├─ config/ │ ├─ settings/ │ │ ├─ base.py │ │ ├─ dev.py │ │ └─ prod.py │ └─ urls.py ├─ env/ │ └─ polling_service/.env ├─ Dockerfile ├─ docker-compose.yml └─ README.md 

---

## 🧪 Testing
bash docker exec -it polling_service pytest 

---

## 🛡️ Environment Variables

| Variable | Description |
|-----------|-------------|
| POSTGRES_USER | PostgreSQL username |
| POSTGRES_PASSWORD | PostgreSQL password |
| POSTGRES_DB | Database name |
| DATABASE_URL | Connection URL |
| DEBUG | Enable/disable debug mode |
| SECRET_KEY | Django secret key |
| AUTH_SERVICE_URL | External authentication service base URL |

---

## 🧩 Future Improvements

- Add Redis caching layer for votes & analytics
- Add WebSocket/async notifications for new votes
- Integrate Celery for background tasks (cleanup jobs)
- Add rate limiting and IP throttling
- Add tagging system for polls

---

## 📝 License
This project is licensed under the MIT License — free to use and modify.