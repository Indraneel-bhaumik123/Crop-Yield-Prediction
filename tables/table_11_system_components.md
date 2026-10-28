# Table 11 System Components

| Subsystem Layer | Module / Component | Technology Stack | Operational Functionality | Production Characteristics |
| --- | --- | --- | --- | --- |
| Machine Learning Engine | Model Pipelines | Scikit-Learn, Joblib | Kharif, Rabi, and Seasonal pipelines combining ColumnTransformer & tuned k-NN | Serialised, sub-millisecond inference, strict zero data leakage. |
| API Gateway | FastAPI Service | FastAPI, Uvicorn, Pydantic v2 | Exposes REST endpoints for prediction, auth, options, and analytics | Asynchronous, self-documenting OpenAPI/Swagger, strict typing. |
| Security & Identity | Authentication Module | OAuth2, JWT, Passlib (Bcrypt) | User registration, password salting & hashing, bearer token issue and verification | Stateless, cryptographic signature validation, 60-min expiration. |
| Data Persistence | Database Layer | SQLite 3, SQLAlchemy ORM | Maintains User table (credentials) and PredictionHistory audit log table | Zero-config embedded relational storage, complete audit trail. |
| User Interface | Frontend Client | HTML5, Vanilla CSS3, JavaScript ES6 | Responsive dashboard with cascading dropdowns, historical records, and chart renders | Clean, glassmorphism aesthetic, zero bloated frontend dependencies. |
