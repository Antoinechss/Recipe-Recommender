# Recipe-Recommender

A recipe recommender that recognizes available ingredients from pictures and returns the best recipe based on available ingredients.

## Features

- 📸 Camera input for ingredient detection
- 🍽️ Recipe recommendations based on detected ingredients
- 🎯 Background removal for better ingredient recognition (requires Python ≤3.12)
- 📱 Mobile-friendly web interface

> **Note:** Background removal functionality requires Python 3.11-3.12. With Python 3.14+, the app will work but show a warning about unavailable background removal.

## Setup

### Prerequisites

- Python 3.11-3.12 (recommended for full functionality)
- Python 3.14+ (basic functionality, background removal unavailable)
- Virtual environment support

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Antoinechss/Recipe-Recommender.git
cd Recipe-Recommender
```

2. Create and activate a virtual environment:

**For full functionality (Python 3.12 - recommended):**
```bash
python3.12 -m venv .venv-py312
source .venv-py312/bin/activate  # On macOS/Linux
# or
.venv-py312\Scripts\activate     # On Windows

# Install full dependencies
pip install -r requirements-full.txt
```

**For basic functionality (Python 3.14+):**
```bash
python -m venv .venv
source .venv/bin/activate        # On macOS/Linux
# or
.venv\Scripts\activate          # On Windows

# Install basic dependencies
pip install -r requirements.txt
```

### Running the Application

You can run the application in several ways:

**Option 1: Using the run script (macOS/Linux) - Automatically selects best environment**
```bash
chmod +x run.sh
./run.sh
```

**Option 2: Direct command with Python 3.12 (recommended)**
```bash
source .venv-py312/bin/activate
streamlit run app/app.py
```

**Option 3: Direct command with Python 3.14+ (basic functionality)**
```bash
source .venv/bin/activate
streamlit run app/app.py
```

**Option 4: Using Python directly**
```bash
# With Python 3.12
.venv-py312/bin/python -m streamlit run app/app.py

# With Python 3.14+
.venv/bin/python -m streamlit run app/app.py
```

The application will be available at `http://localhost:8501`

## Project Structure

```
Recipe-Recommender/
├── app/
│   ├── app.py                    # Main Streamlit application
│   └── object_clipping.py        # Image processing utilities
├── recipe_dataset/
│   ├── data_fix.py               # Data cleaning scripts
│   ├── data_processing.py        # Data preprocessing
│   ├── ingredients_scraper.py    # Ingredient extraction
│   ├── marmiton_recipes.csv      # Recipe dataset
│   ├── recipe_ingredient_matrix.csv
│   ├── recipe_scraper.py         # Recipe data scraping
│   └── recommender.py            # Recommendation engine
├── .streamlit/
│   └── config.toml              # Streamlit configuration
├── requirements.txt             # Python dependencies
├── runtime.txt                  # Python version for deployment
├── run.sh                      # Startup script
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## Dependencies

- `streamlit` - Web application framework
- `Pillow` - Image processing
- `rembg` - Background removal
- `onnxruntime` - Machine learning runtime
- `numpy` - Numerical computing
- `opencv-python` - Computer vision
- `torch` & `torchvision` - Deep learning framework

## Deployment

This project is ready for deployment on platforms like:

- **Heroku**: Uses `runtime.txt` and `requirements.txt`
- **Streamlit Cloud**: Direct deployment from GitHub
- **Docker**: Can be containerized with provided configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).
