# 🚀 **Realtime Sensor Data*

Welcome to the **Realtime Sensor Data**! This is a complete web-based platform designed to monitor and manage sensor data efficiently, featuring a robust **backend** and an interactive **frontend**. The app leverages modern technologies for a seamless user experience.

---

## 📚 **Table of Contents**

1. [Overview](#-overview)
2. [Features](#-features)
3. [Technologies Used](#-technologies-used)
4. [Setup Instructions](#-setup-instructions)
   - [Running with Docker](#-running-with-docker)
5. [Contributing](#️-contributing)
6. [License](#-license)

---

## 🔍 **Overview**

This application allows users to:
- 🔧 Insert, retrieve, and analyze sensor data.
- 📈 Visualize station data with dynamic charts.
- 👨‍💻 Securely manage access with JWT-based authentication.
- 🚀 Easily upload and process CSV files for batch data management.

It includes:
- A **Next.js** frontend for user interaction.
- A **FastAPI** backend for robust API functionality.

---

## 🌟 **Features**

- **Authentication**: Secure login and token-based user authentication.
- **Data Visualization**: Interactive charts for station data.
- **Data Management**: Manage sensors via APIs for data retrieval and processing.
- **CSV Uploads**: Batch upload sensor data using CSV files.
- **Pagination and Sorting**: Navigate and organize station data efficiently.

---

## 🛠 **Technologies Used**

### **Frontend**
- 🌐 **Next.js** (React framework for web applications)
- 🎨 **Tailwind CSS** (Utility-first CSS framework)
- 📊 **Chart.js** (Interactive charts)

### **Backend**
- ⚙️ **FastAPI** (High-performance Python web framework)
- 🗄 **MongoDB** (NoSQL database for data storage)
- 🔐 **JWT** (JSON Web Tokens for authentication)

### **DevOps**
- 🐳 **Docker** (Containerization for easy deployment)
- 🎭 **GitHub Actions** (CI/CD pipeline)

---

## 🛠️ **Setup Instructions**

### 🐳 **Running with Docker**

Follow these steps to run the application using Docker:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/sensor-data-management.git
   cd sensor-data-management
2. **Set up the .env files**:

    Backend: Create a .env file inside backend:

        SECRET_KEY=your_secret_key
        MONGO_URI=mongodb://mongo:27017/sensor_data

    Frontend: Create a .env.local file inside frontend:

        NEXT_PUBLIC_API_URL=http://localhost:8000

3. **Run the application**:

    ```bash
    docker-compose up --build

4. **Access the application**:

    Frontend: http://localhost:3000
    
    Backend: http://localhost:8000/docs

### ❤️ Contributing
Feel free to contribute to this project by submitting issues or pull requests. We appreciate your feedback!

### 📜 License
This project is licensed under the MIT License.

