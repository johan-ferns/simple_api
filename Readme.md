# Simple FastAPI Project

A lightweight API server ready for Azure VM deployment. Built with FastAPI and designed to be extended with ML models.

## Features
- FastAPI api
- Health check endpoint
- Example endpoints ready to extend
- Production-ready with Uvicorn
- Systemd service configuration included

## Local Development

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access the API:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Production Deployment (Azure VM)

See DEPLOYMENT.md for detailed Azure VM setup instructions.
```