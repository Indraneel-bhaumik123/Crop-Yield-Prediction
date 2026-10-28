# 🌾 Seasonal Crop Yield Prediction Using Machine Learning

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Powered-F7931E?logo=scikitlearn&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)
![Frontend](https://img.shields.io/badge/Frontend-HTML%20%7C%20CSS%20%7C%20JavaScript-E34F26?logo=html5&logoColor=white)
![Deployment](https://img.shields.io/badge/Deployment-Render-46E3B7?logo=render&logoColor=black)
![GitHub](https://img.shields.io/badge/Repository-GitHub-181717?logo=github&logoColor=white)

## 📌 Overview

**Seasonal Crop Yield Prediction Using Machine Learning** is a machine learning project designed to estimate agricultural crop yield using historical crop data and relevant environmental factors. The project focuses on three seasonal categories: **Kharif, Rabi, and Seasonal crops**.

The system combines data preprocessing, exploratory data analysis, trained machine learning models, a FastAPI backend, and a web-based frontend to demonstrate how data-driven techniques can support agricultural planning and crop yield estimation.

## 🎯 Project Objectives

- Predict crop yield using relevant agricultural and environmental inputs.
- Analyze crop yield patterns across different seasons.
- Prepare and preprocess datasets for machine learning.
- Train and evaluate machine learning models.
- Store trained models for reuse during prediction.
- Provide prediction functionality through a backend API.
- Build a web interface for user interaction.
- Present model evaluation results through tables and visualizations.

## ✨ Key Features

- **Season-specific prediction:** Supports Kharif, Rabi, and Seasonal crop categories.
- **Machine learning integration:** Includes saved model artifacts for different seasonal datasets.
- **Data analysis:** Includes original and processed datasets, evaluation results, and analysis outputs.
- **Visualizations:** Provides charts for crop distributions, yield patterns, environmental factors, and model comparisons.
- **FastAPI backend:** Exposes application functionality through API routes.
- **Web interface:** Includes HTML, CSS, and JavaScript frontend files.
- **Interactive API documentation:** Supports API exploration through FastAPI's `/docs` endpoint.
- **Testing support:** Includes backend and integration test files.

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| Backend framework | FastAPI |
| ASGI server | Uvicorn |
| Machine learning | Scikit-learn and other project dependencies |
| Frontend | HTML, CSS, JavaScript |
| Data processing | Python data-processing libraries |
| Database | SQLite |
| Model persistence | Joblib |
| Version control | Git and GitHub |
| Deployment platform | Render |

## 📂 Project Structure

```text
Seasonal_Crop_Yield_Prediction_Rebuilt/
│
├── Backend/
│   ├── __init__.py
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── Frontend/
│   ├── favicon.ico
│   ├── index.html
│   ├── prediction.html
│   ├── script.js
│   └── style.css
│
├── data/
│   ├── original/
│   └── processed/
│
├── models/
│   ├── kharif_knn.joblib
│   ├── kharif_model.joblib
│   ├── rabi_knn.joblib
│   ├── rabi_model.joblib
│   ├── seasonal_knn.joblib
│   └── seasonal_model.joblib
│
├── notebooks/
│   └── Seasonal_Crop_Yield_Prediction.ipynb
│
├── results/
│   ├── advanced/
│   ├── faculty_revision/
│   ├── initial_model_evaluation.csv
│   └── tuned_model_evaluation.csv
│
├── figures/
├── tables/
├── tests/
├── references/
├── requirements.txt
├── README.md
└── crop_prediction.db
```

*This tree highlights the main application components. The repository also includes scripts, generated reports, presentation previews, analytical outputs, and supporting research artifacts.*

## ⚙️ Installation and Setup

### Prerequisites

Install the following tools before running the project:

- Python 3
- Git
- Visual Studio Code or another Python-compatible editor

### 1. Clone the Repository

```bash
git clone https://github.com/Indraneel-bhaumik123/Crop-Yield-Prediction.git
```

### 2. Navigate to the Project Folder

```bash
cd Crop-Yield-Prediction
```

### 3. Create a Virtual Environment

**Windows PowerShell**

```powershell
python -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS or Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies

Run this command from the repository root:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 🚀 Running the Application Locally

The backend entry point is `Backend/main.py`.

Start the FastAPI application from the repository root:

```bash
python -m uvicorn Backend.main:app --host 127.0.0.1 --port 8000 --reload
```

After the server starts successfully, open the following addresses.

| Resource | Local URL |
|---|---|
| Web dashboard | http://127.0.0.1:8000/frontend/ |
| Interactive API documentation | http://127.0.0.1:8000/docs |
| API root | http://127.0.0.1:8000/ |

Keep the terminal running while using the application. Press `Ctrl+C` to stop the local server.

## 🧠 Machine Learning Workflow

The project follows a structured machine learning workflow:

1. **Data collection:** Loads the agricultural datasets available in the repository.
2. **Data preprocessing:** Prepares the data for analysis and model evaluation.
3. **Exploratory data analysis:** Examines crop distributions, yield patterns, seasonal variation, and environmental relationships.
4. **Model development:** Uses machine learning models for the relevant seasonal datasets.
5. **Model evaluation:** Compares model performance using appropriate evaluation metrics.
6. **Model persistence:** Stores trained models as Joblib files for reuse.
7. **Backend integration:** Connects saved models to the FastAPI application.
8. **Frontend interaction:** Provides a web interface for interacting with the prediction system.

## 📊 Dataset and Model Artifacts

The repository contains original and processed datasets in the `data/` directory.

The `models/` directory contains saved model artifacts associated with the Kharif, Rabi, and Seasonal categories. These files allow trained models to be loaded for prediction without requiring retraining for every request.

The `results/` and `tables/` directories contain model evaluation outputs, analytical results, and supporting tables. The `figures/` directory contains visualizations used for examining the dataset and presenting analysis results.

**Note:** The required input fields, preprocessing rules, and prediction output format depend on the implementation in the backend and model pipeline.

## 🔌 API Documentation

FastAPI generates interactive API documentation for the implemented routes.

When running locally, visit:

```text
http://127.0.0.1:8000/docs
```

The documentation allows users to inspect and test the API endpoints provided by the application.

For a deployed service, replace the local URL with the actual Render service URL.

## 🧪 Running Tests

The repository includes backend and integration tests in the `tests/` directory.

Run the test suite with:

```bash
python -m pytest
```

If pytest is not installed, install it using:

```bash
python -m pip install pytest
```

Tests may require the project's dependencies, saved model files, and appropriate configuration. Review any failures before treating the application as fully verified.

## ☁️ Deployment on Render

The FastAPI backend can be deployed to Render as a Python Web Service.

### 1. Push Code to GitHub

```bash
git add .
git commit -m "Update project"
git push origin main
```

If Git reports that there are no changes to commit, there is nothing new to commit.

### 2. Create a Render Web Service

1. Open the [Render Dashboard](https://dashboard.render.com/).
2. Select **New → Web Service**.
3. Connect your GitHub account if required.
4. Select the `Crop-Yield-Prediction` repository.
5. Choose the `main` branch.

### 3. Configure Deployment

For a service running from the repository root, use the following settings:

**Root Directory**

Leave blank.

**Build Command**

```bash
pip install -r requirements.txt
```

**Start Command**

```bash
python -m uvicorn Backend.main:app --host 0.0.0.0 --port $PORT
```

Do not use `--reload` in the production command.

Add environment variables only when required by the application's configuration. Do not commit passwords, API keys, or other secrets to the repository.

### 4. Verify the Deployment

After a successful deployment, Render provides a public URL in this format:

```text
https://your-service-name.onrender.com
```

If the backend exposes the frontend at `/frontend/`, the dashboard may be available at:

```text
https://your-service-name.onrender.com/frontend/
```

The API documentation may be available at:

```text
https://your-service-name.onrender.com/docs
```

Replace the example service name with the actual URL provided by Render. The availability of these paths depends on the configured application routes.

**Frontend configuration:** If `Frontend/script.js` uses a hard-coded local API URL such as `127.0.0.1:8000`, update it to use the deployed backend URL so the hosted frontend can communicate with the API.

**Database persistence:** The repository contains an SQLite database file. If the application writes to it, configure persistent storage or an external database as appropriate for production deployment.

## 🔧 Troubleshooting

### `uvicorn` is not recognized

Install dependencies and run Uvicorn through Python:

```bash
python -m pip install -r requirements.txt
python -m uvicorn Backend.main:app --host 127.0.0.1 --port 8000 --reload
```

### Localhost refuses to connect

Check that the server started without errors and is still running in the terminal before opening the browser.

### Render deployment fails

Open the service's **Logs** section and inspect the build or startup error. Common causes include missing dependencies, an incorrect start command, unavailable model files, and incorrect file paths.

### The hosted frontend cannot reach the backend

Check the API URL in `Frontend/script.js`, the configured CORS rules, and whether the backend routes are accessible at the deployed address.

## 🔮 Future Enhancements

- Improve prediction performance through additional model evaluation and tuning.
- Expand support for agricultural datasets and environmental features.
- Strengthen input validation and error handling.
- Improve frontend usability and responsiveness.
- Add monitoring and persistent data storage for production use.

## ✅ Conclusion

Seasonal Crop Yield Prediction demonstrates the use of machine learning, agricultural datasets, and web technologies for crop yield estimation. By combining season-specific model artifacts with a FastAPI backend and frontend interface, the project provides a foundation for exploring data-driven agricultural prediction.

## 👥 Project Authors

This is a **group project** developed by the following contributors:

| Contributor | GitHub Profile |
|---|---|
| **Indraneel Bhaumik** | [@Indraneel-bhaumik123](https://github.com/Indraneel-bhaumik123) |
| **Abhishek Singh** | [@Abhishek-Singh166](https://github.com/Abhishek-Singh166) |
| **Saurabh Singh** | [@Saurabh-Singh158](https://github.com/Saurabh-Singh158) |

---

<p align="center">
  Made with Python, Machine Learning, and teamwork 🌱
</p>

