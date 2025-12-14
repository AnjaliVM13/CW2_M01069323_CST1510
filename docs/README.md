# Multi-Domain Intelligence Platform

<div align="center">

**A professional, multi-domain intelligence platform with AI-powered analytics, role-based access control, and modern cyberpunk UI**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Project Structure](#-project-structure) • [Technologies](#-technologies)

</div>

---
## ⚠️ Important Setup (Required)

To run the project correctly, follow these steps:

1. Open the project folder.
2. Create and activate a virtual environment.
3. If required packages are missing, install all necessary dependencies using:
   pip install -r requirements.txt
4. In the project root directory, create a folder named .streamlit.

5. Inside the .streamlit folder, create a file named secrets.toml.

6. Add the following line inside secrets.toml:
GEMINI_API_KEY = "PASTE YOUR API KEY HERE"

7. Run the application using:
streamlit run Home.py

-----------------------------------------------------------
## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Technologies](#-technologies)
- [Architecture](#-architecture)
- [API Integration](#-api-integration)
- [Database Schema](#-database-schema)
- [Security](#-security)
- [Troubleshooting](#-troubleshooting)
- [Development] 
- [Author]

---

## 🎯 Overview

The **Multi-Domain Intelligence Platform** is a comprehensive web application that integrates three critical business domains:

- **🔐 Cybersecurity Intelligence** - Incident tracking, severity analysis, and threat management
- **📊 Data Governance Analytics** - Dataset metadata management and analytics
- **🛠️ IT Operations Ticketing** - Support ticket management and resolution tracking

Built with **Streamlit** and featuring a modern cyberpunk-themed UI, the platform provides:

- **Role-based access control** (Cyber Security, Data Analyst, IT Support)
- **AI-powered assistant** with Google Gemini API integration
- **Interactive data visualizations** using Plotly
- **CSV data import/export** capabilities
- **Real-time analytics** and reporting
- **Persistent chat history** for AI conversations

---

## ✨ Features

### 🔐 Authentication & Security
- Secure password hashing with **bcrypt**
- Role-based access control (RBAC)
- Session management
- User profile management with avatar uploads

### 📊 Data Management
- **CRUD operations** for all domains
- CSV file upload with column validation
- Manual data entry forms
- Data filtering and search
- Real-time data synchronization

### 🤖 AI Assistant
- **Google Gemini API** integration
- Context-aware responses
- Multiple AI models support (Flash, Pro, 2.0)
- Persistent chat history per user
- Quota management with minimal mode
- Dataset-aware intelligence

### 📈 Visualizations
- Interactive charts with **Plotly**
- Real-time metrics and KPIs
- Trend analysis
- Status distribution charts
- Priority breakdowns

### 🎨 User Interface
- Modern cyberpunk-themed design
- Animated backgrounds and particles
- Glass-morphism effects
- Responsive layout
- Custom Orbitron font styling
- Neon glow effects

### 🔄 Data Import/Export
- CSV upload with validation
- Automatic column matching
- Duplicate detection
- Error handling and reporting
- Manual data entry forms

---

## 🚀 Installation

### Prerequisites

- **Python 3.8+** (recommended: Python 3.10+)
- **pip** package manager
- **Git** (optional, for cloning)

### Step 1: Clone the Repository

```bash
git clone <https://github.com/AnjaliVM13/CST1510>
cd CW2_M01069323_CST1510
```

Or download and extract the ZIP file.

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `streamlit` - Web framework
- `pandas` - Data manipulation
- `bcrypt` - Password hashing
- `google-generativeai` - Gemini API
- `plotly` - Data visualization
- `Pillow` - Image processing
- `numpy` - Numerical computing
- `python-dateutil` - Date parsing
- `sqlite3-binary` - Database driver

### Step 4: Verify Installation

```bash
streamlit --version
python --version
```

---

## ⚙️ Configuration

### 1. Database Setup

The database is automatically created on first run. Ensure the `DATA/` directory exists:

```bash
mkdir DATA
```

### 2. Google Gemini API Key (Optional - for AI features)

1. Get your API key from [Google AI Studio](https://aistudio.google.com/apikey)
2. Create `.streamlit/secrets.toml` file:

```toml
GEMINI_API_KEY = "your-api-key-here"
```

**Note:** Without the API key, AI features will be limited. The simple AI chat (rule-based) will still work.

### 3. Initial Data Files

Place your CSV files in the `DATA/` directory:

```
DATA/
├── users.txt              # User credentials (format: username,password_hash,role)
├── cyber_incidents.csv    # Cybersecurity incidents
├── datasets_metadata.csv  # Dataset metadata
└── it_tickets.csv         # IT support tickets
```

### 4. User Migration

Users are automatically migrated from `DATA/users.txt` on first database setup. Format:

```
username,password_hash,role
Cyber_Guy,$2b$12$...,cyber
Data_Girl,$2b$12$...,data
IT_Man,$2b$12$...,it
```

**Note:** Passwords should be bcrypt hashed. Use the registration page to create new users with plaintext passwords.

---

## 💻 Usage

### Starting the Application

1. **Initialize Database** (First time only):

```bash
python main.py
```

This will:
- Create database tables
- Migrate users from `users.txt`
- Load CSV data
- Display setup summary

2. **Launch Streamlit App**:

```bash
streamlit run Home.py
```

The application will open in your default browser at `http://localhost:8501`

### Application Flow

1. **Login/Register** (`pages/Close.py`)
   - Login with existing credentials
   - Register new account with role selection

2. **Home Dashboard** (`Home.py`)
   - Welcome screen with role-specific information
   - Navigation to domain dashboards

3. **Domain Dashboards**
   - **Cyber Incidents** (`pages/1_Cyber_Incidents.py`) - For `cyber` role
   - **Datasets** (`pages/2_Datasets.py`) - For `data` role
   - **IT Tickets** (`pages/3_IT_Tickets.py`) - For `it` role

4. **Global Features**
   - **AI Assistant** (`pages/4_AI_Assistant.py`) - Available to all users
   - **Profile Settings** (`pages/Profile.py`) - User profile management

### Key Operations

#### CSV Upload
1. Navigate to your domain dashboard
2. Click "Upload CSV" button
3. Select CSV file with matching columns
4. Review matching/unmatching data
5. Confirm insertion

#### Manual Data Entry
1. Click "Add New Entry" button
2. Fill in required fields
3. Submit form
4. Data appears in table immediately

#### AI Assistant Usage
1. Navigate to AI Assistant page
2. Type your question about the data
3. AI provides context-aware responses
4. Chat history is saved automatically

#### Data Visualization
- Interactive charts update in real-time
- Click chart elements for filtering
- Export charts as images
- View detailed statistics

---

## 📁 Project Structure

```
CW2_M01069323_CST1510/
│
├── app/                          # Main application package
│   ├── components/               # Reusable UI components
│   │   ├── sidebar.py           # Navigation sidebar with profile
│   │   ├── ai_chatbox.py        # AI chat interface
│   │   ├── data_manager.py      # CSV upload and data management
│   │   ├── draggable_chatbox.py # Draggable chat component
│   │   ├── floating_ai_chatbox.py # Floating AI chat with Gemini
│   │   └── simple_ai_chat.py    # Rule-based AI chat (no API)
│   │
│   ├── data/                     # Data access layer (Model)
│   │   ├── db.py                # Database connection management
│   │   ├── schema.py            # Database schema definitions
│   │   ├── users.py             # User data operations
│   │   ├── incidents.py         # Cyber incident operations
│   │   ├── tickets.py           # IT ticket operations
│   │   ├── datasets.py          # Dataset metadata operations
│   │   └── chat_history.py      # Chat history persistence
│   │
│   ├── services/                 # Business logic layer
│   │   ├── user_service.py      # Authentication and user management
│   │   ├── ai_assistant.py      # AI assistant service (Gemini)
│   │   └── data_manager.py      # Unified data access service
│   │
│   ├── theme/                    # UI theme and styling
│   │   └── dashboard_effects.py  # Visual effects and animations
│   │
│   ├── dashboard_theme.py        # Legacy theme (backward compatibility)
│   └── theme_base.py             # Base dark theme
│
├── pages/                         # Streamlit page files
│   ├── Close.py                  # Login/Registration page
│   ├── Profile.py                # User profile settings
│   ├── 1_Cyber_Incidents.py      # Cyber incidents dashboard
│   ├── 2_Datasets.py             # Datasets dashboard
│   ├── 3_IT_Tickets.py           # IT tickets dashboard
│   └── 4_AI_Assistant.py         # Global AI assistant
│
├── assets/                        # Static assets
│   ├── profile_pics/             # User profile pictures
│   └── laptop_silhouette.*       # Branding assets
│
├── DATA/                          # Data files and database
│   ├── users.txt                 # User credentials (initial)
│   ├── cyber_incidents.csv       # Sample incident data
│   ├── datasets_metadata.csv     # Sample dataset metadata
│   ├── it_tickets.csv            # Sample ticket data
│   ├── intelligence_platform.db  # SQLite database (auto-generated)
│   └── chat_*.json               # Chat history files (auto-generated)
│
├── chat_data/                     # Additional chat data
├── Test CSV files/                # Test CSV files for validation
│
├── docs/                          # Documentation
│   └── README.md                 # This file
│
├── main.py                        # Database setup script
├── Home.py                        # Main entry point (home dashboard)
├── requirements.txt               # Python dependencies
```

---

## 🛠️ Technologies

### Core Framework
- **Streamlit** - Web application framework
- **Python 3.8+** - Programming language

### Data & Database
- **SQLite** - Relational database
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing

### AI & Machine Learning
- **Google Generative AI (Gemini)** - Large language model API
- **Rule-based AI** - Custom pattern matching for data queries

### Visualization
- **Plotly** - Interactive data visualization
- **Plotly Express** - High-level charting interface
- **Plotly Graph Objects** - Advanced chart customization

### Security & Authentication
- **bcrypt** - Password hashing
- **Session Management** - Streamlit session state

### Image Processing
- **Pillow (PIL)** - Image manipulation for profile pictures

### Utilities
- **python-dateutil** - Date and time parsing
- **Pathlib** - Modern file path handling

---

## 🏗️ Architecture

### MVC-Style Architecture

The application follows a clean **Model-View-Controller** pattern:

```
┌─────────────────────────────────────────┐
│           View Layer (Streamlit)        │
│  pages/*.py, Home.py, components/*.py   │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│        Controller Layer (Services)      │
│  services/user_service.py               │
│  services/ai_assistant.py                │
│  services/data_manager.py                │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         Model Layer (Data Access)       │
│  data/users.py, incidents.py, etc.       │
│  data/db.py, schema.py                   │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│            Database (SQLite)            │
│  intelligence_platform.db               │
└─────────────────────────────────────────┘
```

### Component Architecture

- **Components** - Reusable UI elements (sidebar, chatboxes, data managers)
- **Pages** - Streamlit page files for different views
- **Services** - Business logic and API integrations
- **Data Layer** - Database operations and data models
- **Theme** - UI styling and visual effects

---

## 🔌 API Integration

### Google Gemini API

The platform integrates with Google's Gemini API for AI-powered responses:

**Configuration:**
```toml
# .streamlit/secrets.toml
GEMINI_API_KEY = "your-api-key"
```

**Supported Models:**
- `gemini-1.5-flash` (default, fastest)
- `gemini-1.5-pro` (more capable)
- `gemini-2.0-flash` (latest)
- `gemini-pro` (legacy)

**Features:**
- Context-aware responses
- Dataset-aware intelligence
- Quota management
- Minimal mode (metadata-only) for reduced usage
- Automatic retry with fallback models

**Quota Management:**
- Automatic minimal mode activation on quota errors
- Model fallback chain
- User-friendly error messages
- Usage recommendations

---

## 🗄️ Database Schema

### Tables

#### `users`
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

#### `cyber_incidents`
```sql
CREATE TABLE cyber_incidents (
    incident_id TEXT UNIQUE,
    timestamp TEXT,
    severity TEXT,
    category TEXT,
    status TEXT,
    description TEXT,
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

#### `datasets_metadata`
```sql
CREATE TABLE datasets_metadata (
    dataset_id TEXT UNIQUE,
    name TEXT NOT NULL,
    rows INTEGER,
    columns INTEGER,
    uploaded_by TEXT,
    upload_date TEXT
)
```

#### `it_tickets`
```sql
CREATE TABLE it_tickets (
    ticket_id TEXT UNIQUE NOT NULL,
    priority TEXT,
    description TEXT,
    status TEXT,
    assigned_to TEXT,
    created_at TEXT,
    resolution_time_hours REAL,
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

---

## 🔒 Security

### Authentication
- **Password Hashing**: bcrypt with automatic salt generation
- **Session Management**: Streamlit session state
- **Role-Based Access**: Enforced at page level

### Data Protection
- **SQL Injection Prevention**: Parameterized queries
- **Input Validation**: Column matching and type checking
- **Error Handling**: Graceful error messages without exposing internals

### Best Practices
- Never store plaintext passwords
- Use environment variables for API keys
- Validate all user inputs
- Sanitize file uploads
- Regular database backups recommended

---

## 🐛 Troubleshooting

### Common Issues

#### Database Connection Errors
```bash
# Error: "database is locked"
# Solution: Close other connections, restart the app
```

#### Missing Dependencies
```bash
# Error: "ModuleNotFoundError"
# Solution: pip install -r requirements.txt
```

#### API Key Issues
```bash
# Error: "GEMINI_API_KEY not found"
# Solution: Create .streamlit/secrets.toml with your API key
```

#### Port Already in Use
```bash
# Error: "Port 8501 is already in use"
# Solution: streamlit run Home.py --server.port 8502
```

#### CSV Upload Errors
- Ensure CSV columns match expected format
- Check for special characters in data
- Verify date formats are consistent
- Check file encoding (UTF-8 recommended)

#### Chat History Not Saving
- Verify `DATA/` directory has write permissions
- Check disk space availability
- Review file path permissions

---

## 📝 Development

### Running Tests

```bash
# Run database setup and tests
python main.py
```

### Code Style

The codebase follows:
- PEP 8 Python style guide
- Comprehensive inline comments
- Docstrings for all functions and classes
- Type hints where applicable

### Adding New Features

1. **New Domain**: Add data model in `app/data/`, create page in `pages/`
2. **New Component**: Add to `app/components/`, import in pages
3. **New Service**: Add to `app/services/`, integrate with data layer

---

### Code Guidelines
- Follow PEP 8 style guide
- Add comments for complex logic
- Write docstrings for functions
- Test your changes thoroughly

---

## 👤 Author
- Name: Anjali Marimootoo
- Student ID: M01069323
- Course: CST1510CW2
- Project: Multi-Domain Intelligence Platform

---

</div>

