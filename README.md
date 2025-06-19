
### 📘 `README.md` (Developer Setup Guide)


# 🏭 Arivu Supply Chain System

A modular supply chain management system built with **FastAPI**, **SQLAlchemy**, and **Uvicorn** for Arivu Foods to manage inventory, orders, retailers, and distribution logic.


## ⚙️ Tech Stack

- **FastAPI** – Async API framework
- **SQLAlchemy** – ORM
- **SQLite** – Local dev database (replaceable with PostgreSQL/MySQL)
- **PyJWT** – JWT Authentication
- **Passlib (bcrypt)** – Password hashing
- **Uvicorn** – ASGI server
- **Modular structure** – Per module routes and schemas

---

## 📁 Project Structure

```

supply\_chain\_system/
├── main.py                     # App entry point
├── auth/
│   ├── routes.py               # Login, register, auth logic
│   └── schemas.py              # User, token models
├── inventory/
│   ├── routes.py               # CRUD endpoints
│   └── schemas.py              # Pydantic inventory models
├── database/
│   ├── core.py                 # SQLAlchemy setup
│   └── models.py               # ORM models: User, InventoryItem
...

````

---

## 🚀 Getting Started

### 1. Clone the repo and install dependencies
```bash
git clone https://github.com/yashas-13/arivu
cd arivu
python -m venv arivu-venv
source arivu-venv/bin/activate   # or Scripts\\activate on Windows
pip install -r requirements.txt
````

### 2. Run the app

```bash
uvicorn supply_chain_system.main:app --reload
```

### 3. Access endpoints

* API docs: [http://localhost:8000/docs](http://localhost:8000/docs)
* Auth endpoints: `/auth/login`, `/auth/register`
* Inventory CRUD: `/inventory/`

---

## 🔐 Authentication

All routes (except login/register) require a JWT token.

**Login Response:**

```json
{
  "access_token": "your.jwt.token",
  "token_type": "bearer"
}
```

Use the `Authorization: Bearer <token>` header in requests.

---

## 🧑‍💼 Roles

* **Distributor** – Can manage inventory and orders (formerly `admin`)
* **Retailer** – Can view inventory and place orders

Role is embedded in the JWT and enforced via decorators/middleware.

---

## 🧪 Sample Test User

Register:

```json
{
  "username": "dist1",
  "password": "distpass",
  "role": "distributor"
}
```

---

## 🛠️ Running in Production

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker supply_chain_system.main:app
```

---

## 📊 Future Features

* Real-time WebSocket notifications
* Analytics dashboards
* Role-specific dashboards
* Multi-distributor support

---

## 📄 License

MIT License

````

---

### 🤖 `AGENTS.md` (Agent Definitions for Arivu Foods SCM)


# 🤖 AI & Automation Agents – Arivu Supply Chain System

This file outlines the design and responsibilities of core automation agents in the Arivu Foods supply chain system.

---

## 👥 Roles

| Role         | Description                                      |
|--------------|--------------------------------------------------|
| Distributor  | Manages products, stock, and shipments           |
| Retailer     | Browses products, places orders, tracks delivery |

---

## 🧠 Agents

### 1. 📦 Inventory Management Agent

- Monitors stock levels in real-time
- Automatically flags low-stock items
- Allows distributor to:
  - Add/update/delete inventory items
  - Set reorder thresholds
- Retailers can only **view** stock

**APIs:**
- `GET /inventory/` – list items
- `POST /inventory/` – add item (distributor only)
- `PUT /inventory/{id}` – update (distributor only)
- `DELETE /inventory/{id}` – delete (distributor only)

---

### 2. 🛒 Order Management Agent (planned)

- Retailers place orders
- Distributor approves & dispatches
- Order status tracking
- Future extension: invoice generation

---

### 3. 🧾 Auth Agent

- Handles:
  - User registration/login
  - Role-based access control
  - JWT issuance/validation

**Roles:**
- `"distributor"` → full access to `/inventory`
- `"retailer"` → read-only access

---

## ⚙️ Integration Logic

- **JWT token** contains role
- All protected routes use dependency:
  ```python
  Depends(get_current_user)
````

* Routes apply role checks like:

  ```python
  if user.role != "distributor":
      raise HTTPException(403, "Access denied")
  ```

---

## 📈 Future Agents

* 📬 Notification Agent (e.g. WebSocket updates)
* 📊 Analytics Agent (sales trends, stock turnover)
* 🔁 Auto Reorder Agent (when stock < threshold)

```

Let me know if you'd like these exported to `.md` files or added directly into your GitHub project folder.
```
