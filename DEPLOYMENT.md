# Production Deployment Guide

## Local Development

### Quick Start
```bash
# Clone and setup
git clone https://github.com/Antoinechss/Recipe-Recommender.git
cd Recipe-Recommender

# Setup virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt  # Basic functionality
# OR
pip install -r requirements-full.txt  # With full background removal (Python <= 3.12)

# Run the application
streamlit run app/app.py
```

### Using the Run Script
```bash
chmod +x run.sh
./run.sh
```

## Docker Deployment

### Build and Run with Docker
```bash
# Build the image
docker build -t recipe-recommender .

# Run the container
docker run -p 8501:8501 recipe-recommender
```

### Using Docker Compose
```bash
# Start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

## Cloud Deployment

### Streamlit Cloud
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click

### Heroku
```bash
# Install Heroku CLI and login
heroku login

# Create app
heroku create your-recipe-app

# Set buildpacks (for ML dependencies)
heroku buildpacks:set heroku/python

# Deploy
git push heroku main
```

### Railway
1. Connect your GitHub repository to [Railway](https://railway.app)
2. The app will auto-deploy using the provided configuration

### Google Cloud Platform
```bash
# Build for Cloud Run
gcloud builds submit --tag gcr.io/PROJECT_ID/recipe-recommender

# Deploy to Cloud Run
gcloud run deploy --image gcr.io/PROJECT_ID/recipe-recommender --platform managed
```

## Environment Variables (Optional)

Create a `.env` file for configuration:
```env
STREAMLIT_PORT=8501
STREAMLIT_HOST=0.0.0.0
DEBUG=false
```

## Performance Optimization

### Install Watchdog for Better Performance
```bash
pip install watchdog
```

### Production Settings
- Set `developmentMode = false` in `.streamlit/config.toml`
- Use `--server.headless true` for server deployments
- Consider caching for ML models

## Monitoring

### Health Check Endpoint
The application includes health checks at:
- `http://localhost:8501/_stcore/health`

### Logs
- Application logs are available through Streamlit
- Use `docker-compose logs` for containerized deployments

## Troubleshooting

### Python 3.14 Compatibility
- Some ML libraries (rembg, onnxruntime) don't support Python 3.14 yet
- Use Python 3.11-3.12 for full functionality
- Basic image processing works with Python 3.14

### Memory Issues
- Increase Docker memory if using containers
- Consider using CPU-only versions of ML libraries
- Implement model caching for better performance

### Port Conflicts
- Default port is 8501
- Change in `.streamlit/config.toml` or use `--server.port` flag
