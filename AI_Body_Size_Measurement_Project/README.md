# AI-Based Body Size Measurement System

<div align="center">

![Project Status](https://img.shields.io/badge/status-active-success.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)

**Automated, AI-powered body measurement system for male and female users**

[Features](#features) • [Architecture](#architecture) • [Installation](#installation) • [Usage](#usage) • [Documentation](#documentation)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

The **AI-Based Body Size Measurement System** is a cutting-edge solution that uses computer vision and machine learning to automatically measure male and female body dimensions. The system provides accurate measurements within ±1-2 cm tolerance, enabling perfect clothing fit recommendations and reducing returns in e-commerce.

### Key Objectives

- ✅ Automated measurement of male and female body dimensions using AI
- ✅ Minimize manual errors and returns in clothing purchases
- ✅ Support custom tailoring, fashion e-commerce, and fitness tracking
- ✅ Gender-specific measurement parameters and size recommendations

---

## ✨ Features

### Core Features

- 🎥 **AI-Powered Capture**: Real-time camera-based measurement using pose estimation
- 👤 **Gender-Specific Measurements**: Separate parameters for male and female bodies
- 📏 **High Accuracy**: Measurements within ±1-2 cm tolerance
- ⚡ **Fast Processing**: Results in under 10 seconds
- 📊 **Size Recommendations**: Automatic size suggestions (XS-XXL) with brand mapping
- 📱 **Mobile-Optimized**: Works seamlessly on smartphones and tablets
- 🔒 **Privacy-First**: Automatic image deletion after processing

### User Features

- 👥 **Multi-Profile Support**: Manage measurements for family members
- 📈 **Measurement History**: Track measurements over time
- 🌍 **Multi-Language**: Support for multiple languages
- 🎯 **Fit Preferences**: Choose between slim, regular, or loose fit
- 📤 **Export Data**: Download measurements in PDF/CSV format

### Admin Features

- 📊 **Analytics Dashboard**: Comprehensive metrics and insights
- 👨‍💼 **User Management**: Manage accounts and profiles
- 🤖 **AI Monitoring**: Track model performance and accuracy
- 📐 **Size Chart Management**: Manage brand-specific size mappings
- ✅ **Measurement Validation**: Review and correct flagged measurements

### Advanced Features (Optional)

- 🥽 **AR Virtual Try-On**: Visualize clothing on your body
- 🎨 **3D Avatar Generation**: Create 3D body models
- 📊 **Body Tracking**: Monitor body changes over time
- 💪 **Fitness Analysis**: Posture and fitness recommendations

---

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                         User Browser                         │
│                    (React.js Frontend)                       │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS/REST API
┌────────────────────────▼────────────────────────────────────┐
│                    API Gateway (FastAPI)                     │
├──────────────┬──────────────┬──────────────┬────────────────┤
│ User Service │ Measurement  │ AI Service   │ Admin Service  │
│              │ Service      │              │                │
└──────┬───────┴──────┬───────┴──────┬───────┴────────┬───────┘
       │              │              │                │
       ▼              ▼              ▼                ▼
┌─────────────┐ ┌──────────┐ ┌─────────────┐ ┌──────────────┐
│ PostgreSQL  │ │ MongoDB  │ │ AI Model    │ │ Redis Cache  │
│ (Users,     │ │ (Logs,   │ │ Server      │ │              │
│ Measurements)│ │ Metadata)│ │ (GPU)       │ │              │
└─────────────┘ └──────────┘ └─────────────┘ └──────────────┘
```

### AI Pipeline

```
Image Capture → Preprocessing → Pose Estimation → Body Segmentation
     ↓                                                    ↓
Size Recommendation ← Measurement Calculation ← Keypoint Extraction
```

---

## 🛠️ Technology Stack

### Frontend
- **Framework**: React.js / Next.js
- **Styling**: TailwindCSS
- **State Management**: Redux / Zustand
- **Camera**: WebRTC / MediaDevices API
- **HTTP Client**: Axios

### Backend
- **Framework**: FastAPI (Python) / Express (Node.js)
- **Authentication**: JWT / OAuth 2.0
- **Task Queue**: Celery / Bull
- **Caching**: Redis
- **API Docs**: Swagger / OpenAPI

### AI/ML
- **Pose Estimation**: MediaPipe / OpenPose
- **Segmentation**: Mask R-CNN / DeepLab
- **ML Framework**: TensorFlow / PyTorch
- **Computer Vision**: OpenCV
- **Model Serving**: TensorFlow Serving / ONNX Runtime

### Database
- **Relational**: PostgreSQL
- **Document**: MongoDB
- **Object Storage**: AWS S3 / Google Cloud Storage
- **Cache**: Redis

### DevOps
- **Containerization**: Docker
- **Orchestration**: Kubernetes / Docker Compose
- **CI/CD**: GitHub Actions / Jenkins
- **Cloud**: AWS / Google Cloud / Azure
- **Monitoring**: Prometheus / Grafana

---

## 📁 Project Structure

```
AI_Body_Size_Measurement_Project/
│
├── frontend/                    # React.js frontend application
│   ├── public/                  # Static assets
│   ├── src/
│   │   ├── components/          # Reusable UI components
│   │   │   ├── Camera/          # Camera capture component
│   │   │   ├── MeasurementDisplay/
│   │   │   └── SizeRecommendation/
│   │   ├── pages/               # Page components
│   │   │   ├── Home.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Measurement.jsx
│   │   │   └── History.jsx
│   │   ├── services/            # API integration
│   │   │   ├── api.js
│   │   │   ├── auth.js
│   │   │   └── measurement.js
│   │   ├── styles/              # Global styles
│   │   └── App.js               # Main app component
│   └── package.json
│
├── backend/                     # FastAPI backend application
│   ├── controllers/             # Request handlers
│   │   ├── user_controller.py
│   │   ├── measurement_controller.py
│   │   └── admin_controller.py
│   ├── models/                  # Database models
│   │   ├── user.py
│   │   ├── measurement.py
│   │   └── size_chart.py
│   ├── routes/                  # API routes
│   │   ├── user_routes.py
│   │   ├── measurement_routes.py
│   │   └── admin_routes.py
│   ├── services/                # Business logic
│   │   ├── ai_service.py
│   │   ├── measurement_service.py
│   │   └── size_recommendation.py
│   ├── config/                  # Configuration
│   │   ├── database.py
│   │   └── settings.py
│   ├── app.py                   # Main application
│   └── requirements.txt
│
├── ai_model/                    # AI/ML components
│   ├── pose_estimation/         # Pose detection models
│   │   ├── mediapipe_model.py
│   │   └── inference.py
│   ├── segmentation/            # Body segmentation
│   │   ├── maskrcnn_model.py
│   │   └── preprocessing.py
│   ├── measurement_model/       # Measurement calculation
│   │   ├── regression_model.py
│   │   ├── male_model.py
│   │   └── female_model.py
│   ├── datasets/                # Training data
│   │   ├── male_dataset/
│   │   └── female_dataset/
│   └── training_scripts/        # Model training
│       ├── train_pose.py
│       └── train_measurement.py
│
├── database/                    # Database schemas
│   ├── schema.sql               # PostgreSQL schema
│   └── migrations/              # Database migrations
│
├── docs/                        # Documentation
│   ├── SRS.md                   # Software Requirements Specification
│   ├── API.md                   # API documentation
│   ├── UML_Diagrams/            # System diagrams
│   └── Reports/                 # Project reports
│
├── deployment/                  # Deployment configurations
│   ├── Dockerfile               # Docker configuration
│   ├── docker-compose.yml       # Multi-container setup
│   ├── CI_CD/                   # CI/CD pipelines
│   │   └── github-actions.yml
│   └── cloud_config/            # Cloud deployment configs
│       ├── aws/
│       └── gcp/
│
├── .gitignore
├── README.md
└── LICENSE
```

---

## 🚀 Installation

### Prerequisites

- **Node.js** >= 16.x
- **Python** >= 3.9
- **PostgreSQL** >= 13
- **MongoDB** >= 5.0
- **Redis** >= 6.0
- **Docker** (optional, for containerized deployment)

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
python manage.py migrate

# Start the backend server
python app.py
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your API endpoint

# Start development server
npm run dev
```

### AI Model Setup

```bash
# Navigate to ai_model directory
cd ai_model

# Install AI dependencies
pip install -r requirements.txt

# Download pre-trained models
python download_models.py

# Start AI inference server
python serve_model.py
```

### Docker Setup (Recommended)

```bash
# From project root
docker-compose up -d

# This will start:
# - Frontend (port 3000)
# - Backend (port 8000)
# - PostgreSQL (port 5432)
# - MongoDB (port 27017)
# - Redis (port 6379)
# - AI Model Server (port 5000)
```

---

## 💻 Usage

### For End Users

1. **Register/Login**: Create an account or log in
2. **Select Gender**: Choose Male or Female
3. **Capture Images**: Follow on-screen guidance to capture front, side, and back poses
4. **Get Measurements**: Receive accurate body measurements within seconds
5. **Size Recommendation**: Get clothing size suggestions based on your measurements
6. **View History**: Track your measurements over time

### For Administrators

1. **Access Admin Dashboard**: Login with admin credentials
2. **Monitor System**: View analytics, user statistics, and AI performance
3. **Manage Users**: View and manage user accounts
4. **Validate Measurements**: Review flagged measurements
5. **Update Size Charts**: Add or modify brand-specific size mappings

### API Usage

```javascript
// Example: Get user measurements
const response = await fetch('http://localhost:8000/api/measurements', {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
});

const measurements = await response.json();
```

See [API Documentation](docs/API.md) for complete API reference.

---

## 📚 API Documentation

### Authentication Endpoints

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/refresh` - Refresh access token

### Measurement Endpoints

- `POST /api/measurements/capture` - Upload images for measurement
- `GET /api/measurements` - Get user measurements
- `GET /api/measurements/{id}` - Get specific measurement
- `DELETE /api/measurements/{id}` - Delete measurement

### Size Recommendation Endpoints

- `POST /api/size-recommendation` - Get size recommendation
- `GET /api/size-charts` - Get available size charts
- `GET /api/size-charts/{brand}` - Get brand-specific size chart

### Admin Endpoints

- `GET /api/admin/users` - List all users
- `GET /api/admin/analytics` - Get system analytics
- `PUT /api/admin/measurements/{id}` - Update measurement
- `POST /api/admin/size-charts` - Add new size chart

For complete API documentation, visit `/api/docs` when running the backend server.

---

## 📖 Documentation

- **[Software Requirements Specification (SRS)](docs/SRS.md)** - Complete system requirements
- **[API Documentation](docs/API.md)** - Detailed API reference
- **[Architecture Guide](docs/ARCHITECTURE.md)** - System architecture details
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment instructions
- **[User Manual](docs/USER_MANUAL.md)** - End-user guide
- **[Admin Manual](docs/ADMIN_MANUAL.md)** - Administrator guide

---

## 🧪 Testing

### Run Backend Tests

```bash
cd backend
pytest tests/ -v --cov=.
```

### Run Frontend Tests

```bash
cd frontend
npm test
```

### Run E2E Tests

```bash
npm run test:e2e
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and development process.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Team

- **Project Lead**: [Your Name]
- **AI/ML Engineer**: [Name]
- **Backend Developer**: [Name]
- **Frontend Developer**: [Name]
- **UI/UX Designer**: [Name]

---

## 📞 Support

For support, email support@bodymeasurement.ai or join our Slack channel.

---

## 🙏 Acknowledgments

- MediaPipe team for pose estimation models
- TensorFlow community
- Open-source contributors

---

## 🗺️ Roadmap

- [x] Core measurement functionality
- [x] Gender-specific models
- [ ] AR virtual try-on
- [ ] 3D avatar generation
- [ ] Mobile app (iOS/Android)
- [ ] Smart mirror integration
- [ ] Multi-language support expansion

---

<div align="center">

**Made with ❤️ by the AI Body Measurement Team**

[Website](https://bodymeasurement.ai) • [Documentation](https://docs.bodymeasurement.ai) • [Blog](https://blog.bodymeasurement.ai)

</div>
